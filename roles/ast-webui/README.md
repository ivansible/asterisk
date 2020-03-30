# ivansible.ast_webui

[![Github Test Status](https://github.com/ivansible/ast-webui/workflows/Molecule%20test/badge.svg?branch=master)](https://github.com/ivansible/ast-webui/actions)
[![Travis Test Status](https://travis-ci.org/ivansible/ast-webui.svg?branch=master)](https://travis-ci.org/ivansible/ast-webui)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-ivansible.ast__webui-68a.svg?style=flat)](https://galaxy.ansible.com/ivansible/ast_webui/)

This role configures Web UI in Nginx for Asterisk and Gigaset.


## Requirements

None


## Variables

    ast_webui_server: ~
Front server name eg. `webui.example.com`.

    ast_webui_lecert: ~
Name of custom letsencrypt certificate for the server (optional).

    ast_webui_bindip: 127.0.0.1
IP addresses where nginx listens.

    ast_webui_origin: 192.168.1.1
Host name or IP address of the origin server.

    ast_webui_cloudflare_email: ~
    ast_webui_cloudflare_token: ~
CloudFlare DNS credentials. If these are empty, then DNS task will be skipped.


## Tags

- `ast_webui_all` -- all tasks


## Dependencies

- `ivansible.nginx_base` - inherit defaults and handlers
- `ivansible.lin_nginx`    (implicit dependency)


## Example Playbook

    - hosts: server
      roles:
         - role: ivansible.ast_webui
           ast_webui_server: webui.example.com
           ast_webui_origin: 192.168.11.2


## License

MIT


## Author Information

Created in 2020 by [IvanSible](https://github.com/ivansible)
