#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_generate_root
version_added: "3.14.0"
short_description: Hashicorp Vault generate_root module
description:
    - Module to (update) generate_root Hashicorp Vault.
options:
    url:
        description:
            - url for vault
        default: to environment variable VAULT_ADDR
    ca_cert:
        description:
            - "path to a PEM-encoded CA cert file to use to verify the Vault server TLS certificate"
        default: to environment variable VAULT_CACERT
    ca_path:
        description:
            - "path to a directory of PEM-encoded CA cert files to verify the Vault server TLS certificate : if ca_cert is specified, its value will take precedence"
        default: to environment variable VAULT_CAPATH
    client_cert:
        description:
            - "path to a PEM-encoded client certificate for TLS authentication to the Vault server"
        default: to environment variable VAULT_CLIENT_CERT
    client_key:
        description:
            - "path to an unencrypted PEM-encoded private key matching the client certificate"
        default: to environment variable VAULT_CLIENT_KEY
    verify:
        description:
            - "if set, do not verify presented TLS certificate before communicating with Vault server : setting this variable is not recommended except during testing"
        default: to environment variable VAULT_SKIP_VERIFY
    authtype:
        description:
            - "authentication type to use: token, userpass, github, ldap, approle"
        default: token
    token:
        description:
            - token for vault
        default: to environment variable VAULT_TOKEN
    username:
        description:
            - username to login to vault.
        default: to environment variable VAULT_USER
    password:
        description:
            - password to login to vault.
        default: to environment variable VAULT_PASSWORD
    key:
        description:
            - vault key shard.
    nonce:
        description:
            - generate_root nonce.
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_generate_root:
      key: '{{vault_unseal_key}}'
      nonce: '{{nonce}}'
'''


def main():
    argspec = hashivault_argspec()
    argspec['key'] = dict(required=False, type='str')
    argspec['nonce'] = dict(required=True, type='str')
    module = hashivault_init(argspec)
    result = hashivault_generate_root(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
from ansible.module_utils.hashivault import *


@hashiwrapper
def hashivault_generate_root(params):
    key = params.get('key')
    nonce = params.get('nonce')
    client = hashivault_client(params)
    return {'status': client.generate_root(key, nonce), 'changed': True}


if __name__ == '__main__':
    main()
