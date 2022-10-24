# Burp Collaborator Server Ansible Role

Strongly inspired by 4ARMED work (https://github.com/4ARMED/terraform-burp-collaborator) and Anshumanbh (https://github.com/anshumanbh/terraform-burp-collaborator). Thank you very much to them.

# Additions and modifications
  - Adding specific options to burp_collaborator_config file to manage polling ports number and the specific associated AWS Security-Group.
  - Forked from the 4ARMED Ansible role hosted on Ansible-Galaxy, a local role is used to avoid relying on Ansible-Galaxy.
  - The setup of Java JRE is also integrated in the Ansible playbook.
  - The directives for SSL certificates management has been updated in the Burp Collaborator config file.
  - Quick fix in main.tf files
  - main.tf has been modified to match Ubuntu 22.04 on Free Tier instance.

Installs [Burp Collaborator Server](https://portswigger.net/burp/) on a Ubuntu 22.04 Linux host.

## Requirements

- Debian-based Linux target
- Unix/Linux-based Ansible 2.2 machine with openssl installed
- Burp Suite Professional jar file (https://portswigger.net/burp/)

## Role Variables

```
burp_http_port: 80
burp_https_port: 443
burp_dns_port: 53
burp_smtp_port: 25
burp_smtp_port2: 587
burp_smtps_port: 465
burp_http_polling_port: 9090
burp_https_polling_port: 9443
burp_metrics_path: metricated
burp_whitelist: '["127.0.0.1"]'
burp_key: burp.pk8
burp_cert: burp.crt
burp_ca_bundle: intermediate.crt
burp_server_domain: collaborator.example.com
burp_local_address: <internal IP address>
burp_public_address: <public IP address> # May be the same as above
```

If you would like Ansible to generate you a self-signed cert for use with Collaborator complete the following, otherwise set `generate_self_signed_certs` to `false`.

`
generate_self_signed_certs: true
country: GB
state: London
locality: London
organisation: Corp
organisational_unit: Training
`

### License

MIT/BSD

### Author Information

Initially created by [@marcwickenden](https://twitter.com/marcwickenden) at [4ARMED](https://www.4armed.com/).
Inspired by Anshumanbh
Finally updated by [@KarK](https://twitter.com/KarKKca)
