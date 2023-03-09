#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
module: metal_ip_assignment
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.state
short_description: Create/delete a ip_assignment in Equinix Metal
description:
    - Create/delete a ip_assignment in Equinix Metal.
options:
    name:
        description:
            - The name of the ip_assignment.
        type: str
    id:
        description:
            - UUID of the ip_assignment.
        type: str
    organization_id:
        description:
            - UUID of the organization to create the ip_assignment in.
        type: str
    payment_method_id:
        description:
            - UUID of payment method to use for the ip_assignment. When blank, the API assumes default org payment method.
        type: str
    customdata:
        description:
            - Custom data about the ip_assignment to create.
        type: str
    backend_transfer_enabled:
        description:
            - Enable backend transfer for the ip_assignment.
        type: bool
'''

EXAMPLES = r'''
- name: Create new ip_assignment
  hosts: localhost
  tasks:
      equinix.cloud.metal_ip_assignment:
          name: "new ip_assignment"

- name: Create new ip_assignment within non-default organization
  hosts: localhost
  tasks:
      equinix.cloud.metal_ip_assignment:
          name: "my org ip_assignment"
          organization_id: a4cc87f9-e00f-48c2-9460-74aa60beb6b0

- name: Remove ip_assignment by id
  hosts: localhost
  tasks:
      equinix.cloud.metal_ip_assignment:
          state: absent
          id: eef49903-7a09-4ca1-af67-4087c29ab5b6

- name: Create new ip_assignment with non-default billing method
  hosts: localhost
  tasks:
      equinix.cloud.metal_ip_assignment:
          name: "newer ip_assignment"
          payment_method_id: "abf49903-7a09-4ca1-af67-4087c29ab343"
'''

RETURN = r'''
id:
    description: UUID of the ip_assignment.
    returned: I(state=present)
    type: str
    sample: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
name:
    description: Name of the ip_assignment.
    returned: I(state=present)
    type: str
    sample: "new ip_assignment"
organization_id:
    description: UUID of the organization the ip_assignment belongs to.
    returned: I(state=present)
    type: str
    sample: "a4cc87f9-e00f-48c2-9460-74aa60beb6b0"
payment_method_id:
    description: UUID of the payment method used for the ip_assignment.
    returned: I(state=present)
    type: str
    sample: "abf49903-7a09-4ca1-af67-4087c29ab343"
customdata:
    description: Custom data about the ip_assignment.
    returned: I(state=present)
    type: str
    sample: '{"setting": 12}'
backend_transfer_enabled:
    description: Whether backend transfer is enabled for the ip_assignment.
    returned: I(state=present)
    type: bool
    sample: true
'''

from ansible.module_utils._text import to_native
import traceback

from ansible_specdoc.objects import (
    SpecField,
    FieldType,
    SpecReturnValue,
)

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
    getSpecDocMeta,
)

module_spec = dict(
    id=SpecField(
        type=FieldType.string,
        description="UUID of the ip_assignment.",
    ),
    device_id=SpecField(
        type=FieldType.string,
        description="UUID of the device to assign the IP to.",
    ),
    address=SpecField(
        type=FieldType.string,
        description="IP address to assign to the device.",
    ),
    customdata=SpecField(
        type=FieldType.dict,
        description="Custom data about the ip_assignment to create.",
    ),
    manageable=SpecField(
        type=FieldType.bool,
        description="Whether the IP address is manageable.",
    ),
)

specdoc_examples = [
    '''
    - name: request ip reservation
      equinix.cloud.metal_reserved_ip_block:
        type: "public_ipv4"
        metro: "sv"
        quantity: 1
        project_id: "{{ project.id }}"
      register: ip_reservation

    - name: available addresses from reservation
      equinix.cloud.metal_available_ips_info:
        reserved_ip_block_id: "{{ ip_reservation.id }}"
        cidr: 32
      register: available_ips
    
    - assert:
        that:
          - "available_ips.available | length == 1"  


    - name: create device
      equinix.cloud.metal_device:
        project_id: "{{ project.id }}"
        hostname: "device1"
        operating_system: ubuntu_20_04
        plan: c3.small.x86
        metro: sv
        state: present
      register: device

    - name: assign available IP
      equinix.cloud.metal_ip_assignment:
        device_id: "{{ device.id }}"
        address: "{{ available_ips.available[0] }}"
      register: assignment
''',
]

result_sample = []

MUTABLE_ATTRIBUTES = [
    k for k, v in module_spec.items() if v.editable
]

SPECDOC_META = getSpecDocMeta(
    short_description='Manage Equinix Metal IP assignments',
    description='Asign reserved IPs to Equinix Metal devices.',
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "metal_ip_assignment": SpecReturnValue(
            description='The assignment object.',
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        required_one_of=[("device_id", "id")],
        required_by=dict(device_id=["address"]),
    )

    state = module.params.get("state")
    changed = False

    try:
        module.params_syntax_check()
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_ip_assignment", tolerate_not_found)
        else:
            fetched = module.get_one_from_list(
                "metal_ip_assignment",
                ["device_id", "address"],
            )

        if fetched:
            module.params['id'] = fetched['id']
            if state == "present":
                diff = get_diff(module.params, fetched, MUTABLE_ATTRIBUTES)
                if diff:
                    module.fail_json(msg="Cannot update metal_ip_assignment: %s" % diff)
            else:
                module.delete_by_id("metal_ip_assignment")
                changed = True
        else:
            if state == "present":
                fetched = module.create("metal_ip_assignment")
                if 'id' not in fetched:
                    module.fail_json(msg="UUID not found in ip_assignment creation response")
                changed = True
            else:
                fetched = {}
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg="Error in metal_ip_assignment: {0}".format(to_native(e)),
                         exception=tb)

    fetched.update({'changed': changed})
    module.exit_json(**fetched)


if __name__ == '__main__':
    main()
