# ivansible.asterisk_soho

This role extends core Asterisk deployment configured by
[ivansible.asterisk_core](https://github.com/ivansible/asterisk-core)
for work in a small office with a few SIP phones and several
accounts registered on a single SIP gateway provider.


## Requirements

None


## Role Variables

Some variables are inherited from the `asterisk_base` role,
see them in the _Dependencies_ section.
Role-specific variables are listed below, along with default values.

    ast_soho_gateway_alias: gateway
    ast_soho_phones_alias: phones
Aliases are used in many places in this role to produce full names of
generated dialplan contexts, rule-sets, SIP peer groups and ACL rules
for gateway and phones.

    ast_soho_gateway_codecs: "g729,g722,ulaw,alaw"
    ast_soho_phones_codecs: "g729,g722,ulaw,alaw"
These are just comma-separated lists of Asterisk codec modules allowed
for gateway provider and phones in order of preference.

    ast_soho_gateway_hosts:
      - sip1.voip-provider.com
      - sip2.voip-provider.com
A list of provider host names. Incoming calls from provider will be
accepted from all these hosts. Outgoing calls will be placed through
the *first* host in the list (via a specific account).

    ast_soho_gateway_networks:
      - 192.168.0.0/16
As a security measure, we not only check provider host name in incoming
INVITE requests, but also limit allowed IP ranges. A dedicated ACL rule
will be configured in Asterisk from this white list of IP networks.

    ast_soho_gateway_accounts:
      - name: gw-account1
        username: 4215
        password: secret1
        active: yes
      - name: gw-account2
        username: 4216
        password: secret2
        active: no
A list of account credentials for placing outgoing calls through provider.
Each account can be connected with a few phones in the `ast_soho_phones`
list. Outgoing calls from a phone will placed via the connected account.
Incoming calls from provider account will ring all connected phones until
one of them answers. Only active accounts will be configured.

For security reasons, you should go to the provider website and limit
accepted IPs for these accounts by the IP address of your Asterisk host.

Please note that we dont't register with gateway provider to accept incoming
calls. You should manually configure the accounts on provider website
so that when gateway calls us back, it provides a callback extension
with specific account name in the SIP URL, like
`gw-account1@my.asterisk.domain.com` or `gw-account2@my.asterisk.domain.com`.
All incoming calls will land in a dialplan context generated right for that.

    ast_soho_phones:
      - name: phone1
        password: secret
        exten: 101
        gateway: account1
        active: yes
Each SIP phone will have a SIP peer configured in Asterisk with `name` for
username and `password` for specific secret. The `gateway` field should
point to an existing gateway account `name` from the list above.

All phones can reach each other via `exten` extension numbers.

For convenience, phones can make outgoing calls through any configured account,
not only the associated one, by prefixing the number with `exten*`, where
`exten` is extension of the phone via whose provider we are placing the call.
For example, if a phone with extension `123` has associated gateway account
`account3`, then any other phone can make a call to extension `123*7495613`,
and this call will routed via `account3` to the number `7495613` on gateway.

    ast_soho_phones_networks:
      - ; My Local Network
      - 192.168.0.0/16
Most SIP phones on the market do not support TLS yet, so this role
has to enable less secure TCP/UDP SIP access. To improve security,
you should limit accepted IP ranges allowed to login.
This role will generate a white-list ACL for SIP phones
Entries in the list are IP ranges of the form "ip.address/prefix".
Entries that start from semicolon `;` are comments.

    ast_soho_gateway_billing_exten: ""

Many VOIP providers have a specific extension associated with accounts.
A call to this extension activates a simple voice attendant, which
tells remaining account balance or tariff details.

If this setting is a non-empty string, calls from our sip-phones
to a predefined extension `*100#` will redirect to the provider billing
extension via associated account.

For convenience, phones can reach billing information of each other by
dialing a short `*exten#` extension. For example, dialing `*123#`
will route to the billing extension of the gateway account associated
with a phone on extension `123`.

    ast_soho_quick_numbers:
      - name: my close friend
        exten: 111
        number: +1-212-123-4567

Also you can add a few short numbers to the dialplan. Please note that
calls to quick numbers will be placed through the first active gateway account.


## Dialplan Notes

The `asterisk_core` could have added softphones to the Asterisk configuration.
This role arranges dialplan contexts in such a way that all sip-phones can
call softphones and softphones can call sip-phones. Both softphones and
sip-phones will have access to the daytime service (extension `100`).
Also, softphones can make outgoing calls through gateway accounts by prefixing
number with `exten*`, like sip-phones themselves.


## Tags

- `ast_soho_all`


## Dependencies

This role inherits defaults and handlers from
[ivansible.asterisk_base](https://github.com/ivansible/asterisk-base).

List of inherited variables (only used variables are listed):
  - ast_experimental
  - ast_dialplan_hints
  - ast_default_language
  - ast_default_codecs
  - ast_qualify_value

List of inherited handlers:
  - restart asterisk service (not used)
  - reload asterisk service

Also this role depends on
[ivansible.asterisk_core](https://github.com/ivansible/asterisk-core),
but this dependency is not recorded in meta information.
You should explicitly include `asterisk_core` in your playbook before
this role, as shown in the example below. This approach avoids repetitive
execution of time-consuming base role, when several dependent roles are used.


## Example Playbook

    - hosts: asterisk.example.com
      roles:
         - role: ivansible.asterisk_core
           ast_reset: yes
           ast_ip_list:
             - 192.168.1.21
           ast_softphones: []
         - role: ivansible.asterisk_soho
           ast_soho_gateway_billing_exten: "*105#"
           ast_soho_gateway_accounts:
             - name: account1
               username: 42115
               password: secret
           ast_soho_gateway_hosts:
             - sip.example.com
           ast_soho_phones:
             - name: phone1
               password: secret
               exten: 101
               gateway: account1
               active: yes


## License

MIT

## Author Information

Created in 2018 by [IvanSible](https://github.com/ivansible)
