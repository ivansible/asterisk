# ivansible.ast_core

This role deploys basic asterisk server on a linux host.
This is a core deployment to be extended by other asterisk-related roles.
The role will:
  - install asterisk system packages for asterisk;
  - install additional packages for SIP debugging and audio conversion (sox);
  - configure asterisk for postgresql database access;
  - configure SSL certificates;
  - create SIP and dialplan templates suitable for multi-role asterisk deployment;
  - configure SIP peers for softphones;
  - deploy a simple daytime voice service;
  - enable G729 codec support;
  - configure custom music-on-hold;
  - optionally limit CPU quota for asterisk service;
  - open SIP, TLS, RTP in linux firewall;
  - configure local AMI over TCP/HTTP, but block AMI ports from remote access;
  - configure syslog and log rotation;
  - enable NTP synchronization and step-sync host time;
  - give ansible remote user access to asterisk.


## External Files

The following external files are required by this role:

    ast_moh_mp3_tarball_url
Tarball with music-on-hold sounds in MP3 format.

    ast_sounds_extras_wav_url
Extra sounds in WAV format required by the daytime AGI script.

    ast_g729_codec_url
G729 codec module from http://asterisk.hosting.lv which is optimal
for target host.

    ast_g729_bench_free_tarball_url
Tarball with shell script and a set of free G729 codec modules
to choose the best one.

    ast_g729_bench_digium_tarball_url
Tarball with digium utilities to becnhmark various G729 codec flavors.

    ast_pg_dump_url
AES-encrypted tarball with asterisk database dump.
For details about encryption, please refer to role
[backup_base](https://github.com/ivansible/backup-base).


## Inherited Variables

Inherited variables are listed below, along with default values.

    ast_reset: false  (inherited from ast_base)

If `true`, the role will reset all configuration files to their initial state
before adjusting particular options. Also, database will be always fully reset
from saved dump. If `false`, the dump is applied only when a new database is created.

    ast_experimental: false
Enables use of TCP TOS.

    ast_ssl_cert: /etc/ssl/certs/ssl-cert-snakeoil.pem
    ast_ssl_key: /etc/ssl/private/ssl-cert-snakeoil.key
Path of SSL certificate and private key files,
which asterisk will use for TLS conections.

    ast_domains: "{{ [ ansible_fqdn ] }}"
The list of domains that asterisk will accept for incoming calls.
The first domain is default and used for outgoing calls.

    ast_dialplan_hints: true
    ast_default_language: en
    ast_default_codecs: g729,g722,ulaw,alaw
    ast_qualify_value: 'yes'
    ast_local_dir: /usr/local/asterisk
These variables are inherited from the `ast_base` role.

    ast_pg_host: localhost
    ast_pg_port: 5432
    ast_pg_dbname: asterisk
    ast_pg_user: asterisk
    ast_pg_pass: secret
Database connection parameters.

Variables inherited from the role `lin_base`:
  - flag `lin_use_rsyslog` enables use of rsyslog and logrotate with asterisk
  - flag `lin_compress_logs` enables/disables compression of rotated logs


## Role Variables

Available variables are listed below, along with default values.

    ast_ip_list: ...
List of exteranlly visible host addresses.
You can customize this list if automatic ansible discovery fails.

    ast_default_nat: true
If `true`, asterisk will treat all incoming requests the identically
and reply to the IP port from where a request has come.
If `false`, asterisk will by default the port set in the `rport` directive.
This is less secure as remote attacker can find user names of configured
peers depending on the asterisk reply.

    ast_softphones:
      - name: softphone1
        password: secretpass1
        exten: 101
        srtp: false
        active: true
List of SIP and dialplan parameters for softphones.
Name and password define username and incoming secret for softphone SIP peer.
Extension `exten` defines how softphone will be accesible from dialplan.

    ast_softphones_secure: true
If `true`, softphones will be required to connect via TLS and use SRTP only.
However, you can still enable plain RTP for a particular softphone using
the `srtp` per-phone setting.

    ast_user_agent: Asterisk PBX 13.18
Changes default user agent in SIP replies and in SDP descriptors.

    ast_voicemail_pass: 1234
Default voicemail password.

    ast_record_file: /tmp/asterisk-record.wav
Location where voice recording service (extension 97)
will save recorded sound.

    ast_pg_dump_url: ""
If this is not empty, the role will reset database from given dump.

    ast_params_default: ...
    ast_params_group: []
    ast_params_host: []
You can use these to adjust host-specific asterisk options.

    ast_sip_port: 5060
    ast_tls_port: 5061
    ast_rtp_port_start: 10100
    ast_rtp_port_end: 10300
    ast_ami_port: 5038
    ast_http_port: 8088
    ast_https_port: 8089
Various ports.

    ast_sip_limit: 1/sec
    ast_sip_burst: 9
Set limit on SIP transactions per second (if `limit` is not an empty string).

    ast_hackers_max_hits: 100
Disable hosts that make more connection attempts than given limit.

    ast_ami_admin_password: ast-ami-secret
AMI adminitrator user password. By default only administrator
with full access is configured.

    ast_sip_allowed_networks: any
SIP port 5060 will be open only for given networks in the Ubuntu firewall.
Default is all networks.

    ast_reject_networks: []
Completely reject requests to SIP and TLS ports from IPs on these networks.
Default is none. Set this if you are attacked by SIP hackers.
Each network is defined in format like `172.12.0.0/17`.

The new iptables rules will be placed directly in the ufw file
`/etc/ufw/before.rules` in the block `ANSIBLE reject sip hackers`
destined for the chain `ufw-before-input`.

    ast_prefer_ipv4: false
If `true`, GLIBC DNS resolver is configured to prefer IPV4.
If `false`, GLIBC resolver will return addresses as received (no preference).
If unset, the file `/etc/gai.conf` will not be modified.

    ast_stun_addr: ""
If not empty, this address will be configured in `rtp.conf`.
Examples:
```
    stun.tld.com
    stun.tld.com:3478
    "172.1.2.3"
    "172.1.2.3:3478"
```
If the string is empty, STUN and ICE will be disabled.

    ast_ntp_server: ""
If not empty, installation will step-sync host time to the given NTP server.
By default we do not do this to save some playbook time.
If syncing is important, set time server to something like `2.pool.ntp.org`.

    ast_cpu_quota: false
CPU quota.
Examples: `5% 60% 100% false`

    ast_logrotate_timer: daily
Rotate asterisk logs: daily or weekly

    ast_modules_preload: ...
`res_odbc` is preloaded to allow for dynamic configuration.
`res_speech` is preloaded as a workaround for loader warning
`"loading module 'res_agi.so': undefined symbol: ast_speech_change"`.

    ast_modules_noload: ...
Disables obsolete, buggy or unused modules. By default we disable
PJSIP, ARI and modules that warn about undefined symbols in
Asterisk 13.1 on Ubuntu Xenial.

    ast_packages_install: ...
List of APT packages to install:
- core asterisk packages
- format-agnostic asterisk sound packages
- asterisk modules for playing MP3 natively
- utilities for converting moh files between MP3/WAV formats
- standard Ubuntu SSL certificates
- python3 for AGI
- postgresql database client packages and ODBC
- utilities for sip debugging
- NTP for time synchronization
and more


## Tags

In the execution order:

    ast_install
    ast_packages
Install system packages for asterisk, network and SIP troubleshooting,
audio format conversion, database access and ODBC.

    ast_sudo
(In `ast_install`).
Configures sudo to let asterisk daemon invoke a few commands as root.

    ast_ipv4
(In `ast_install`).
Depending on options, configures GLIBC resolver to prefer IPV4 over IPV6.

    ast_ssl
Grants asterisk unix user access to configured SSL certificate and private key.

    ast_g729
Downloads and installs a chosen G729 codec module.

    ast_g729_bench
(In `ast_g729`).
Installs performance benchmark to choose between different G729 codec implementations.

    ast_config
Configures core asterisk systems: logger, module loader, voicemail, RTP.
Also adjusts various scattered options.

    ast_moh
Downloads tarball with music-on-hold sounds in MP3 format.
Converts MP3 music into WAV to reduce service CPU load.
Configures music-on-hold.

    ast_daytime
Installs AGI script that tells current system time. Downloads and unpacks
external tarball with extra WAV sounds required by the script.
Creates symbolic links for extra sounds in the asterisk sound locations.

    ast_database
Creates user and database for asterisk on the database server.
Restores database content from a downloaded dump.
Configures ODBC and asterisk res_odbc and func_odbc modules.

    ast_dialplan
Configures core _sip.conf_ and _extensions.conf_.

    ast_systemd
    ast_cpu_quota
Enables asterisk service and optionally limits CPU quota.

    ast_firewall
Opens SIP, TLS and RTP ports for asterisk. Blocks AMI TCP/HTTP ports.

    ast_hackers
Creates cron job to disable annoying password hackers.

    ast_timesync
Asterisk requires precise time for sound bridging to work correctly.
This step installs and enables NTP synchronization on host.

    ast_user
Adds bash alias `astcli` for running asterisk CLI to remote ansible user.
This user is added to the `asterisk` group for access to asterisk CLI.


## Dependencies

This role inherits defaults and handlers from `ivansible.ast_base`.

List of inherited variables (only variables actually used are listed):
  - ast_reset
  - ast_experimental
  - ast_ssl_cert
  - ast_ssl_key
  - ast_domains
  - ast_dialplan_hints
  - ast_default_language
  - ast_default_codecs
  - ast_qualify_value

List of inherited handlers:
  - restart asterisk service
  - reload asterisk service  (not used)

This role also inherits the following handlers from `ivansible.lin_base`:
  - reload systemd daemon
  - reload ubuntu firewall

The following roles are imported directly from tasks:
  - ivansible.lin_docker  (installs docker for digium G729 benchmark)
  - ivansible.dev_user    (prepares local bash rc file)

Some other roles depend on this one, but inclusion should be done explicitly
in playbook to avoid repetitive execution.

This role invokes task `postgresql_db_restore_encrypted.yml`
from role `ivansible.backup_base` and uses default encryption secret.


# Music-On-Hold

Later you can add more music-on-hold MP3 files to the
`/usr/local/asterisk/moh/mp3/` directory.
After modification, run the following commands as user `asterisk`:
```
   /usr/local/asterisk/bin/moh-mp3-to-wav.sh
   asterisk -rx "moh reload"
```


## SIP Peers

The main asterisk SIP configuration file `/etc/asterisk/sip.conf`
is made modular by means of `#include`s.

Asterisk roles that require external registrations should add snippets
`register => xxx` in the files `sip.d/<rolename>.register.conf`
under directory `/etc/asterisk`.

Asterisk roles that define peers should add snippets with peer sections
in the files `sip.d/<rolename>.peers.conf` under directory `/etc/asterisk`.


## Dialplan

This role disables LUA and AEL dialplan modules and removes
corresponding configurations. We opt for the old-school asterisk dialplan.

The main asterisk dialplan configuration file `/etc/asterisk/extensions.conf`
is made modular by means of `#include`s.

Roles can put utility dialplan snippets in files `dialplan.d/<rolename>.common.conf`
and rule groups and contexts in the files `dialplan.d/<rolename>.rules.conf`.
These files are `#include`d in the filename alphanumeric order.

This role adds some convenient dialplan services available from softphones:
  - current time service (extension `100`);
  - voice recording service (extension `97`);
See details in the file `dialplan.d/services.common.conf`.

This role also provides some common macros and subroutines in the file
`dialplan.d/macros.common.conf` in the `[sub]` global context.
Dialplan subroutines `phone` and `provider` should be used as:
```
    Gosub(sub,phone,1,(<phone_peer_name_without_sip_prefix>))
    Gosub(sub,provider,1,(<provider_peer_name_without_sip_prefix>,<provider_extension>))
```

For security, only the characters `0123456789*#` (see global variable `SAFECHARS`)
are allowed in a `Dial` extension. All other characters are filtered out.


### Auto-attendant Menus

Creating auto-attendant menus poses a problem. All menus are similar but
putting menu template in a common context does not work because all
extensions available from menu should be known in advance and be present
in this template context or nested contexts.

As a solution, this role creates menu snippet without a context and puts
in the `/etc/asterisk/dialplan.d/menu.conf` file. Other role that needs
a menu should create a new context, add menu-accessible extensions,
then include the menu snippet, like:
```
    [role-context]
    #include dialplan.d/menu.conf
    exten => extension1,1,...
    exten => extension2,1,...
    #include context.d/rolename.conf
```

*Note*: Menu inclusions cause the following warning, which is okay:
```"Same File included more than once!", This data will be saved in xxx~~1```.


### Dialplan Contexts and Security

Roles can create dialplan contexts cross-referenced from other roles.
Since roles can be installed in random order, we use included context
files in `/etc/asterisk/context.d/<rolename>.conf` of the form:
```
    include => <context1>
    include => <context2>
```

Roles group extensions in low-level extension contexts, which can be included
in access-level grouping contexts. Access-level contexts are assigned to peers
or peer groups and usually have name `[peergroup-home]`.
Example:
```
    [extension-group-A]
    exten => extensionA1,1,...
    exten => extensionA2,1,...

    [extension-group-B]
    exten => extensionB1,1,...
    exten => extensionB2,1,...

    [extension-group-C]
    exten => extensionC1,1,...
    exten => extensionC2,1,...

    [internal_peers-home]
    include => extension-group-A
    include => extension-group-B

    [external_peers-home]
    include => extension-group-C
```


## ACLs

If the peers IP addresses should be limited, please create ACL definitions
in the files `/etc/asterisk/acl.d/<rolename>.conf`. Asterisk combines
ACLs with `AND` logic, so if ACLs cover different IP ranges, the result
will always be to reject. Therefore, every ACL should cover ALL addresses
for a particular peer role.

This role contains a task group for creating white-list ACLs,
which can be invoked in other asterisk roles as follows:
```
- include_role:
    name: ivansible.ast_core
    tasks_from: _acl.yml
  vars:
    acl: <acl_name>
    networks:
    - ; comment
    - 192.168.0.0/16
    - ...
```
The empty network list means "permit all".


## Features

The following features are configured:
```
automon=*3
automixmon=*4
blindxfer=*5
atxfer=*6
disconnect=*0
```

Dialplan subroutines named `phone` and `provider` wrap the `Dial` application
for use in various asterisk roles. Currently, only the `disconnect` feature
is enabled (the `h` flag, see Asterisk documentation).

*Note*: The `phone` subroutine enables music-on-hold (`m`),
but subroutine `provider` does not.


## Requirements

None


## Example Playbook

    - hosts: asterisk.example.com
      roles:
         - role: ivansible.ast_core
           ast_reset: true
           ast_ip_list:
             - 192.168.1.21
           ast_softphones:
             - name: softphone1
             - password: secretpass1
             - exten: 101
             - srtp: false
             - active: true


## License

MIT

## Author Information

Created in 2018-2020 by [IvanSible](https://github.com/ivansible)
