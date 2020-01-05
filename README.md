# Community Hass.io Add-ons: Lutron Certificate

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
[![License][license-shield]](LICENSE.md)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

[![GitLab CI][gitlabci-shield]][gitlabci]
![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

A simple utility to generate signed certificate files to allow local control of
a Lutron Caseta smart bridge.

## About

This add-on will guide you through the necessary steps to create signed
certificate files necessary to control your Lutron Caseta smart bridge with
Home Assistant.

Three files will be created during successful execution of the wizard:

- `/ssl/lutron/caseta.key`: the private key file used to generate the
  certificate.
- `/ssl/lutron/caseta.crt`: the signed certificate file used to connect to
  the Lutron Caseta bridge.
- `/ssl/lutron/caseta-bridge.crt`: the certificate authority file that is
  downloaded from the Lutron Caseta bridge.

Be sure to add Lutron Caseta to your `configuration.yaml` after starting the
add-on:

```yaml
lutron_caseta:
  host: 192.168.1.100
  keyfile: /ssl/lutron/caseta.key
  certfile: /ssl/lutron/caseta.crt
  ca_certs: /ssl/lutron/caseta-bridge.crt
```

For more information on how to configure Lutron Caseta in Home Assistant see
the [Lutron Caseta documentation][lutron-caseta-docs].

## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Hass.io add-on.

1. Search for the “Lutron Certificate” add-on in the Hass.io 166 add-on store
   and install it.
1. Start the "Lutron Certificate" add-on.
1. Check the logs of the "Lutron Certificate" add-on to see if everything went well.
1. Open the web UI for the "Lutron Certificate" add-on and follow the steps.
1. Configure [Lutron Caseta][lutron-caseta-docs] in your `configuration.yaml` file.

## Configuration

Even though this add-on is just a basic add-on, it does come with some
configuration options to play around with.

**Note**: _Remember to restart the add-on when the configuration is changed._

Lutron Certificate add-on configuration:

```json
{
  "log_level": "info"
}
```

### Option: `log_level`

The `log_level` option controls the level of log output by the add-on and can
be changed to be more or less verbose, which might be useful when you are
dealing with an unknown issue. Possible values are:

- `trace`: Show every detail, like all called internal functions.
- `debug`: Shows detailed debug information.
- `info`: Normal (usually) interesting events.
- `warning`: Exceptional occurrences that are not errors.
- `error`:  Runtime errors that do not require immediate action.
- `fatal`: Something went terribly wrong. Add-on becomes unusable.

Please note that each level automatically includes log messages from a
more severe level, e.g., `debug` also shows `info` messages. By default,
the `log_level` is set to `info`, which is the recommended setting unless
you are troubleshooting.

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of ``MAJOR.MINOR.PATCH``. In a @xxxxshell, the version will be incremented
based on the following:

- ``MAJOR``: Incompatible or major changes.
- ``MINOR``: Backwards-compatible new features and enhancements.
- ``PATCH``: Backwards-compatible bugfixes and package updates.

## Support

Got questions?

You have several options to get them answered:

- The [Community Hass.io Add-ons Discord chat server][discord] for add-on
  support and feature requests.
- The [Home Assistant Discord chat server][discord-ha] for general Home
  Assistant discussions and questions.
- The Home Assistant [Community Forum][forum].
- Join the [Reddit subreddit][reddit] in [/r/homeassistant][reddit]

You could also [open an issue here][issue] GitHub.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We have set up a separate document containing our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Authors & contributors

The original setup of this repository is by [Dale Higgs][dale3h].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## We have got some Hass.io add-ons for you

Want some more functionality to your Hass.io Home Assistant instance?

We have created multiple add-ons for Hass.io. For a full list, check out
our [GitHub Repository][repository].

## License

MIT License

Copyright (c) 2018-2020 Dale Higgs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/dale3h
[commits-shield]: https://img.shields.io/github/commit-activity/y/hassio-addons/addon-lutron-cert.svg
[commits]: https://github.com/hassio-addons/addon-lutron-cert/commits/master
[contributors]: https://github.com/hassio-addons/addon-lutron-cert/graphs/contributors
[dale3h]: https://github.com/dale3h
[discord-ha]: https://discord.gg/c5DvZ4e
[discord-shield]: https://img.shields.io/discord/478094546522079232.svg
[discord]: https://discord.me/hassioaddons
[dockerhub]: https://hub.docker.com/r/hassioaddons/lutron-cert
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/t/community-hass-io-add-on-lutron-certificate/70317
[gitlabci-shield]: https://gitlab.com/hassio-addons/addon-lutron-cert/badges/master/pipeline.svg
[gitlabci]: https://gitlab.com/hassio-addons/addon-lutron-cert/pipelines
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[issue]: https://github.com/hassio-addons/addon-lutron-cert/issues
[keepchangelog]: https://keepachangelog.com/en/1.0.0/
[license-shield]: https://img.shields.io/github/license/hassio-addons/addon-lutron-cert.svg
[lutron-caseta-docs]: https://www.home-assistant.io/components/lutron_caseta/
[maintenance-shield]: https://img.shields.io/maintenance/yes/2020.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[reddit]: https://reddit.com/r/homeassistant
[releases-shield]: https://img.shields.io/github/release/hassio-addons/addon-lutron-cert.svg
[releases]: https://github.com/hassio-addons/addon-lutron-cert/releases
[repository]: https://github.com/hassio-addons/repository
[semver]: https://semver.org/spec/v2.0.0.html
[version-shield]: https://images.microbadger.com/badges/version/hassioaddons/lutron-cert.svg
