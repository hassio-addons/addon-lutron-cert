"""
Server to get Lutron Caseta certificate.
"""
import json
import os
import re
import requests
import socket
import ssl

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from urllib.parse import urlencode

################################################################################

SSL_PATH = "/ssl/lutron"
KEY_FILE = "%s/caseta.key" % SSL_PATH
CERT_FILE = "%s/caseta.crt" % SSL_PATH
CA_FILE = "%s/caseta-bridge.crt" % SSL_PATH

################################################################################

LOGIN_SERVER = "device-login.lutron.com"
APP_CLIENT_ID = ("e001a4471eb6152b7b3f35e549905fd8589dfcf57eb680b6fb37f20878c"
                 "28e5a")
APP_CLIENT_SECRET = ("b07fee362538d6df3b129dc3026a72d27e1005a3d1e5839eed5ed18"
                     "c63a89b27")
APP_OAUTH_REDIRECT_PAGE = "lutron_app_oauth_redirect"
CERT_SUBJECT = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Pennsylvania"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Coopersburg"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                       "Lutron Electronics Co., Inc."),
    x509.NameAttribute(NameOID.COMMON_NAME, "Lutron Caseta App")
])

BASE_URL = "https://%s/" % LOGIN_SERVER
REDIRECT_URI = "https://%s/%s" % (LOGIN_SERVER, APP_OAUTH_REDIRECT_PAGE)

AUTHORIZE_URL = ("%soauth/authorize?%s" % (BASE_URL,
                                           urlencode({
                                               "client_id": APP_CLIENT_ID,
                                               "redirect_uri": REDIRECT_URI,
                                               "response_type": "code"
                                           })))

################################################################################

def ensure_path():
    """Create SSL path if it does not exist."""
    if not os.path.isdir(SSL_PATH):
        os.makedirs(SSL_PATH, exist_ok=True)

################################################################################

def get_private_key():
    """Get the private key file used to generate the certificate."""
    try:
        with open(KEY_FILE, 'rb') as f:
            private_key = load_pem_private_key(f.read(), None,
                                               default_backend())
    except FileNotFoundError:
        private_key = rsa.generate_private_key(public_exponent=65537,
                                               key_size=2048,
                                               backend=default_backend())

        ensure_path()
        with open(KEY_FILE, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
    return private_key

################################################################################

def get_certificate(oauth_code):
    """Get the certificate file used to generate the CA file."""
    try:
        with open(CERT_FILE, 'rb') as f:
            certificate = x509.load_pem_x509_certificate(f.read(),
                                                         default_backend())
    except FileNotFoundError:
        private_key = get_private_key()

        csr = (x509.CertificateSigningRequestBuilder()
               .subject_name(CERT_SUBJECT)
               .sign(private_key, hashes.SHA256(), default_backend()))

        if not oauth_code:
            raise ValueError("Received invalid OAuth code. Please try again.")

        token = requests.post("%soauth/token" % BASE_URL, data={
            'code': oauth_code,
            'client_id': APP_CLIENT_ID,
            'client_secret': APP_CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'}).json()

        if 'error' in token:
            raise ValueError(token['error_description'])

        if token.get('token_type') != 'bearer':
            raise ValueError("Received invalid token %s. Try generating a "
                             "new code (one time use)." % token)

        access_token = token['access_token']

        pairing_request_content = {
            'remote_signs_app_certificate_signing_request':
            csr.public_bytes(serialization.Encoding.PEM).decode('ASCII')
        }

        pairing_response = requests.post(
            "%sapi/v1/remotepairing/application/user" % BASE_URL,
            json=pairing_request_content,
            headers={
                'X-DeviceType': 'Caseta,RA2Select',
                'Authorization': 'Bearer %s' % access_token
            }
        ).json()

        app_cert = pairing_response['remote_signs_app_certificate']
        remote_cert = pairing_response['local_signs_remote_certificate']

        ensure_path()
        with open(CERT_FILE, 'wb') as f:
            f.write(app_cert.encode('ASCII'))
            f.write(remote_cert.encode('ASCII'))

################################################################################

def get_ca_cert(server_addr):
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = ssl.wrap_socket(raw_socket, keyfile=KEY_FILE,
                                 certfile=CERT_FILE,
                                 ssl_version=ssl.PROTOCOL_TLSv1_2)

    ssl_socket.connect((server_addr, 8081))

    ca_der = ssl_socket.getpeercert(True)
    ca_cert = x509.load_der_x509_certificate(ca_der, default_backend())

    ensure_path()
    with open(CA_FILE, 'wb') as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

    ssl_socket.send(("%s\r\n" % json.dumps({
        'CommuniqueType': 'ReadRequest',
        'Header': {'Url': '/server/1/status/ping'}
    })).encode('UTF-8'))

    while True:
        buffer = b''
        while not buffer.endswith(b'\r\n'):
            buffer += ssl_socket.read()

        leap_response = json.loads(buffer.decode('UTF-8'))
        if leap_response['CommuniqueType'] == 'ReadResponse':
            break

    ssl_socket.close()

    return leap_response

################################################################################

# Flask webserver
app = Flask(__name__)

# Flask app config
with open('/var/lib/dbus/machine-id', 'r') as f:
    app.secret_key = f.read()

@app.route('/', methods=['GET', 'POST'])
def wizard():
    """Show the current step based on progress."""
    if os.path.isfile(CA_FILE):
        leap_version = session.get('leap_version')
        if leap_version is not None:
            flash("Successfully connected to bridge, running LEAP Server"
                  "version %s" % leap_version, 'success')

        return render_template(
            'success.html',
            server_addr=session.get('server_addr', '192.168.1.100'),
            ssl_path=SSL_PATH,
            ssl_files={'key_file': KEY_FILE,
                       'cert_file': CERT_FILE,
                       'ca_file': CA_FILE})

    if os.path.isfile(CERT_FILE):
        return render_template(
            'bridge.html',
            server_addr=session.get('server_addr', ''))

    return render_template('login.html', authorize_url=AUTHORIZE_URL)

@app.route('/reset')
def reset():
    """Delete certificate files and session data."""
    try:
        # Remove certificate files
        os.remove(KEY_FILE)
        os.remove(CERT_FILE)
        os.remove(CA_FILE)

        # Clear session data
        session.clear()
    except FileNotFoundError:
        pass

    # Alert user that session has been reset
    flash("The certificate files have been deleted and your session "
          "has been reset.", 'warning')

    return redirect(url_for('wizard'))

@app.route('/debug')
def debug():
    """Output session data for debugging."""
    values = {k: v for (k, v) in session.items()}
    values.update({
        'key_file': (KEY_FILE, os.path.isfile(KEY_FILE)),
        'cert_file': (CERT_FILE, os.path.isfile(CERT_FILE)),
        'ca_file': (CA_FILE, os.path.isfile(CA_FILE)),
    })
    return app.response_class(response=json.dumps(values),
                              status=200,
                              mimetype='application/json')

################################################################################

@app.route('/process_url', methods=['POST'])
def process_url():
    """Process the redirect URL."""
    redirected_url = request.form.get('redirected_url')
    oauth_code = re.sub(r'^(.*?code=){0,1}([0-9a-f]*)\s*$', r'\2',
                        redirected_url)

    try:
        get_certificate(oauth_code)
    except ValueError as err:
        flash(str(err), 'danger')

    return redirect(url_for('wizard'))

@app.route('/process_addr', methods=['POST'])
def process_addr():
    """Process the bridge IP address/hostname."""
    server_addr = request.form.get('server_addr')
    session['server_addr'] = server_addr

    try:
        leap_response = get_ca_cert(server_addr)
        session['leap_version'] = leap_response['Body'] \
                                  ['PingResponse']['LEAPVersion']
    except ConnectionRefusedError:
        flash("A connection to %s could not be established. Please check "
              "the IP address and try again." % server_addr, 'danger')

    return redirect(url_for('wizard'))

################################################################################

def main():
    """Main program routine."""
    # Make sure SSL_PATH exists
    ensure_path()

    # Start flask server
    app.run(host='0.0.0.0', port=5817)

################################################################################

if __name__ == '__main__':
    main()
