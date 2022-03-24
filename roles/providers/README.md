# ivansible.ast_providers

This role extends core Asterisk deployment configured by
[ivansible.ast_core](https://github.com/ivansible/ast-core)
with calls via few SIP providers.


## Requirements

None


## Variables

    ast_providers: ...
`ast_providers` is an array of records with the following fields:

    name: provider1
Provider name is used in this role as a basis for SIP peer name and
for ACL rule name.

    exten: 5
`exten` defines how calls via a specific provider can be placed from
`softphones` (created by [ast_core](https://github.com/ivansible/ast-core))
and `sipphones` (created by [ast_soho](https://github.com/ivansible/ast-soho)).

    prepend: ""
`prepend` by default is an empty string.
Example: if `exten` is `67` and `prepend` is `99`, then calling `67*12345`
will place a call to `9912345` through the given provider.

    host: sip.provider1.com
Host / domain name of the SIP provider.

    domain: 195.168.1.5
Domain defaults to the host setting and normally not needed, only
for rare providers with tricky configuration.

    username: 12345
    password: secret123
Provider credentials to use when placing outward calls
and to register for inward calls.

    transport: tcp
Comma-separated list of _udp,tcp,tls_ transports. The first transport
will be user for outward calls. Optional with default: _udp,tcp_.

    networks:
      - 172.16.0.0/17    # ip network
      - 192.168.1.5/32   # ip host
      - 0.0.0.0/0        # all
A dedicated ACL rule will be configured in Asterisk from this
white list of IP networks. Empty list means _permit all IPs_.

    codecs: g729,ulaw,alaw
Comma-separated list of codecs. Optional with default `ast_default_codecs`.

    language: en
Language for sound prompts. Optional with default `ast_default_language`.

    active: true
If this boolean is `false`, provider will be excluded from configuration.


## Tags

- `ast_providers_all`


## Dependencies

1. This role inherits defaults and handlers from
   [ivansible.ast_base](https://github.com/ivansible/ast-base).

   List of inherited variables (only used variables are listed):
    - `ast_default_language`
    - `ast_default_codecs`

   List of inherited handlers:
    - `restart asterisk service` (not used)
    - `reload asterisk service`

2. This role inherits few variables from the role
   [ivansible.ast_soho](https://github.com/ivansible/ast-soho).

   List of inherited variables (only used variables are listed):
    - `ast_soho_phones_alias`
    - `ast_soho_gateway_alias`

3. Also this role depends on
   [ivansible.ast_core](https://github.com/ivansible/ast-core),
   but this dependency is not recorded in meta information.
   You should explicitly include `ast_core` in your playbook before
   this role, as shown in the example below. This approach avoids repetitive
   execution of time-consuming base role, when several dependent roles are used.


## Example Playbook

    - hosts: asterisk-box
      roles:
         - role: ivansible.ast_providers


## License

MIT

## Author Information

Created in 2018-2020 by [IvanSible](https://github.com/ivansible)
