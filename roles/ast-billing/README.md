# ivansible.ast_billing

This role extends core Asterisk deployment configured by
[ivansible.ast_core](https://github.com/ivansible/ast-core)
with tariff parser and trunk selector.


## Requirements

None


## Variables

Available variables are listed below, along with default values.

    ast_billing_dir: "{{ ansible_user_dir }}/devel/asterisk-billing"

    ast_billing_options:
      - section: dialer
        option: log_file
        value: /var/log/asterisk/dialer.log
      - section: dialer
        option: db_host
        value: "{{ ast_pg_host }}"
      - section: dialer
        option: db_port
        value: "{{ ast_pg_port }}"

    ast_billing_secrets:
      - name: pgsql
        user: "{{ ast_pg_user }}"
        pass: "{{ ast_pg_pass }}"


## Tags

- `ast_billing_all`
- `lin_ssh_known_hosts`


## Dependencies

This role inherits defaults and handlers from
[ivansible.ast_base](https://github.com/ivansible/ast-base).

List of inherited variables (only used variables are listed):
  - ast_pg_host: localhost
  - ast_pg_port: 5432
  - ast_pg_dbname: asterisk
  - ast_pg_user: asterisk
  - ast_pg_pass: secret

List of inherited handlers:
  - restart asterisk service (not used)
  - reload asterisk service

Also this role depends on
[ivansible.ast_core](https://github.com/ivansible/ast-core),
but this dependency is not recorded in meta information.
You should explicitly include `ast_core` in your playbook before
this role, as shown in the example below. This approach avoids repetitive
execution of time-consuming base role when several dependent roles are used.

To enable `gitlab.com` public key, this role imports task `known_hosts.yml`
from the role [ivansible.lin_ssh](https://github.com/ivansible/lin-ssh#tags).


## Example Playbook

    - hosts: my_box
      roles:
         - role: ivansible.ast_billing


## License

MIT

## Author Information

Created in 2018-2020 by [IvanSible](https://github.com/ivansible)
