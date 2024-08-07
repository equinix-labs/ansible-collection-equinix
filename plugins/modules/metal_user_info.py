#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and RETURN are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = r"""
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Gather information about the current user for Equinix Metal
module: metal_user_info
notes: []
options:
  metal_api_token:
    description:
    - The Equinix Metal API token to use.
    required: true
    type: str
  metal_api_url:
    description:
    - The Equinix Metal API URL to use.
    required: true
    type: str
requirements: null
short_description: Gather information about the current user for Equinix Metal
"""
EXAMPLES = r"""
- name: Gather information about the current current user
  hosts: localhost
  tasks:
  - equinix.cloud.metal_user_info:
      metal_api_token: '{{ lookup(''env'', ''METAL_API_TOKEN'') }}'
    register: result
  - debug:
      var: result
"""
RETURN = r"""
user:
  description: Information about the current user.
  returned: always
  sample:
  - avatar_thumb_url: https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm
    avatar_url: https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm
    created_at: '2019-08-24T14:15:22Z'
    customdata: {}
    default_organization_id: 7498eaa8-62af-4757-81e0-959250fc9cd5
    email: john.doe@email.com
    emails:
    - href: string
    first_name: John
    full_name: John Doe
    href: /metal/v1/users/497f6eca-6276-4993-bfeb-53cbbbba6f08
    id: 497f6eca-6276-4993-bfeb-53cbbbba6f08
    last_login_at: '2019-08-24T14:15:22Z'
    last_name: Doe
    max_projects: 0
    short_id: 497f6eca
    timezone: America/New_York
    two_factor_auth: ''
    updated_at: '2019-08-24T14:15:22Z'
  type: dict
"""

# End of generated documentation

from ansible.module_utils._text import to_native
from ansible_specdoc.objects import (
    SpecField,
    FieldType,
    SpecReturnValue,
)
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    getSpecDocMeta,
)

# Define module specifications
module_spec = dict(
    metal_api_token=SpecField(
        type=FieldType.string,
        description=['The Equinix Metal API token to use.'],
        required=True,
        no_log=True,
    ),
    metal_api_url=SpecField(
        type=FieldType.string,
        description=['The Equinix Metal API URL to use.'],
        required=True,
    ),
)

# Define examples for the module documentation
specdoc_examples = [
    '''
- name: Gather information about the current current user
  hosts: localhost
  tasks:
    - equinix.cloud.metal_user_info:
        metal_api_token: "{{ lookup('env', 'METAL_API_TOKEN') }}"
      register: result

    - debug:
        var: result
''',
]

# Define return values for the module documentation
return_values = [
    {
        "avatar_thumb_url": "https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm",
        "avatar_url": "https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm",
        "created_at": "2019-08-24T14:15:22Z",
        "customdata": {},
        "default_organization_id": "7498eaa8-62af-4757-81e0-959250fc9cd5",
        "email": "john.doe@email.com",
        "emails": [
            {
                "href": "string"
            }
        ],
        "first_name": "John",
        "full_name": "John Doe",
        "href": "/metal/v1/users/497f6eca-6276-4993-bfeb-53cbbbba6f08",
        "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
        "last_login_at": "2019-08-24T14:15:22Z",
        "last_name": "Doe",
        "max_projects": 0,
        "short_id": "497f6eca",
        "timezone": "America/New_York",
        "two_factor_auth": "",
        "updated_at": "2019-08-24T14:15:22Z"
    }
]

# Define the metadata for SpecDoc
SPECDOC_META = getSpecDocMeta(
    short_description='Gather information about the current user for Equinix Metal',
    description='Gather information about the current user for Equinix Metal',
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "user": SpecReturnValue(
            description='Information about the current user.',
            type=FieldType.dict,
            sample=return_values,
        ),
    },
)

def main():
    # Create an instance of EquinixModule with provided specifications
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        is_info=True,
    )
    try:
        # Check for syntax validity in provided parameters
        module.params_syntax_check()

        # Setting the id parameter to 'current_user' ensures the module fetches the correct information
        # Since the id parameter is required by 'get_by_id', we need to set it to a value
        module.params["id"] = "current_user"

        # Fetch the current user's information using the get_by_id method
        result = module.get_by_id("metal_user")

        # Prepare the return value with the fetched user information
        return_value = {"user": result}
    except Exception as e:
        # Capture any exception and fail the module execution with the error message
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)

    # Exit the module with the return value
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
