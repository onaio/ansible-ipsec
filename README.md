Ansible IPSEC
=========

Install [Strongswan](https://www.strongswan.org/) and configure IPSEC.

Requirements
------------

The role has been developed and tested on Debian/Ubuntu 18.0.4

The controller requires Ansible 2.10 or newer. Task imports, restart
notifications and template rendering were checked locally with ansible-core
2.20. Package and service actions were mocked. These checks do not validate
a running VPN on a new Ubuntu release.

Role Variables
--------------
These are the role variables and default values
```yaml
ipsec_config_setup:
  uniqueids: 'yes'
  charonstart: 'yes'
  charondebug: ''
ipsec_conn_default: {}
ipsec_conn_groups: {}
ipsec_secrets: []
```
## `ipsec_config_setup`
Configures general configuration parameters. A list of available options can be found on [StrongSwan config setup section documentation](https://wiki.strongswan.org/projects/strongswan/wiki/ConfigSetupSection)

## `ipsec_conn_default`
Defaults for connections. This will populate the default conn (%default)
All conn groups inherit the parameters defined in a conn `%default`

Example:

```yaml
  strongswan_conn_default:
   type: "tunnel"
   keyexchange: "ikev1"
   ikelifetime: "3h"
   lifetime: "1h"
   left: "%any"
```
Refer to the conn section for a list of all the parameters

## `ipsec_conn_groups`
In Strongswan `ipsec.conf` configuration, conn defines a connection. The full list of available parameters can be found on [StrongSwan Conn section documentation](https://wiki.strongswan.org/projects/strongswan/wiki/ConnSection)
`ipsec_conn_groups` specifies the connections to be added to the `ipsec.conf`.

Each key represents the name of a connection. The subelemets that the connection has is any valid conn parameter for a connection.

Example:
```yaml
ipsec_conn_groups:
      group1:
        right: "10.10.10.9"
        rightsubnet: "192.168.10.0/24"
        ike: "aes256-sha1-modp1024"
        esp: "aes256-sha1-modp1024"
        auto: "start"
      group2:
        authby: "secret"
        keyexchange: "ikev1"
        left: "%defaultroute"
        leftid: "3.7.150.3"
        leftsubnet: "142.40.37.8/32"
        right: "11.2.1.0"
        rightsubnet: "192.168.1.10/32"
        auto: "route"
        ike: "aes256-sha1-modp1024"
        esp: "aes256-sha1-modp1024"
```
## `ipsec_secrets`
Defines a list of secrets to be added to the ipsec secret file `ipsec.secrets`
Full documentation for the secrets file can be found [here](https://wiki.strongswan.org/projects/strongswan/wiki/IpsecSecrets)

 `ipsec_secrets` should be a list that contains the following attributes:
  - left:      Any valid ID selector. (optional)
  - right:     Any valid ID selector
  - type:       Optional (defaults to PSK) - any valid secret type
  - credentials: Required - Connection's credentials, e.g the preshared password

Example:

```yaml
ipsec_secrets:
      - right: "11.2.1.0"
        left: "3.7.150.3"
        type: "PSK"
        credentials: "presharedpassword"
```

Dependencies
------------

`onaio.monit` must be available on the controller. Its tasks run only when
`ipsec_enable_monit` is true.

Example Playbook
----------------


```yml
- hosts: ipsec_peer
  roles:
      - role: onaio.ipsec
```
License
-------

Apache V2

Author Information
------------------

[Ona](https://ona.io) Engineering.
