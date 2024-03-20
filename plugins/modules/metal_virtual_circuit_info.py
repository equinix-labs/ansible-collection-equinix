#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and METAL_PROJECT_ARGS are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Gather information about Equinix Metal Virtual Circuits
module: metal_virtual_circuit_info
notes: []
options:
  connection_id:
    description:
    - ID of the virtual circuit resource
    required: false
    type: str
  organization_id:
    description:
    - ID of the organisation to which the virtual circuit belongs
    required: false
    type: str
requirements: null
short_description: Gather information about Equinix Metal Virtual Circuits
'''
EXAMPLES = '''
- name: Gather information about all projects in an organization
  hosts: localhost
  tasks:
  - equinix.cloud.metal_virtual_circuit_info:
      organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
'''
RETURN = '''
resources:
  description: Found resources
  returned: always
  sample:
  - backend_transfer_enabled: false
    customdata: {}
    description: ''
    id: 31d3ae8b-bd5a-41f3-a420-055211345cc7
    name: ansible-integration-test-project-csle6t2y-project2
    organization_id: 70c2f878-9f32-452e-8c69-ab15480e1d99
    payment_method_id: 845b45a3-c565-47e5-b9b6-a86204a73d29
  type: dict
'''

# End

from ansible.module_utils._text import to_native
from ansible_specdoc.objects import SpecField, FieldType, SpecReturnValue
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    getSpecDocMeta,
)

module_spec = dict(
    connection_id=SpecField(
        type=FieldType.string,
        description=['ID of the virtual circuit resource'],
    ),
    organization_id=SpecField(
        type=FieldType.string,
        description=["ID of the organisation to which the virtual circuit belongs"],
    ),
)

specdoc_examples = ['''
- name: Gather information about all projects in an organization
  hosts: localhost
  tasks:
      - equinix.cloud.metal_virtual_circuit_info:
          organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
''']

return_values = [
  {
    "backend_transfer_enabled": False,
    "customdata": {},
    "description": "",
    "id": "31d3ae8b-bd5a-41f3-a420-055211345cc7",
    "name": "ansible-integration-test-project-csle6t2y-project2",
    "organization_id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
    "payment_method_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
  }
]

SPECDOC_META = getSpecDocMeta(
    short_description="Gather information about Equinix Metal Virtual Circuits",
    description=(
        'Gather information about Equinix Metal Virtual Circuits'
    ),
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "resources": SpecReturnValue(
            description='Found resources',
            type=FieldType.dict,
            sample=return_values,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        is_info=True,
    )
    try:
        module.params_syntax_check()
        if module.params.get('connection_id'):
            return_value = {'resources': module.get_list("metal_virtual_circuit")}
        else:
            module.fail_json(msg="missing connection_id parameter")

    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
