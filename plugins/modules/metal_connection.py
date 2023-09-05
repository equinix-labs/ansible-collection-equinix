#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and RETURN are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Manage the interconnection in Equinix Metal. You can use *id* or *name*
  to lookup the resource. If you want to create new resource, you must provide *project_id*,
  *name*, *type*, *redundancy* and *speed*.
module: metal_connection
notes: []
options:
  contact_email:
    description:
    - Email for the person to contact for inquires.
    required: false
    type: str
  description:
    description:
    - Description of the connection.
    required: false
    type: str
  id:
    description:
    - UUID of the connection.
    required: false
    type: str
  metro:
    description:
    - Metro where the connection will be created
    required: false
    type: str
  mode:
    description:
    - Mode for connections in IBX facilities with the dedicated type - standard or
      tunnel
    required: false
    type: str
  name:
    description:
    - Name of the connection resource
    required: false
    type: str
  project_id:
    description:
    - UUID of the project this connection belongs to.
    required: false
    type: str
  redundancy:
    description:
    - Connection redundancy - redundant or primary
    required: false
    type: str
  service_token_type:
    description:
    - Only used with shared connection. Type of service token to use for the connection,
      a_side or z_side
    required: false
    type: str
  speed:
    description:
    - Port speed. Required for a_side connections. Allowed values are ['50Mbps', '200Mbps',
      '500Mbps', '1Gbps', '2Gbps', '5Gbps', '10Gbps']
    required: false
    type: int
  tags:
    description:
    - Tags attached to the connection
    elements: str
    required: false
    type: int
  type:
    description:
    - Connection type - dedicated or shared
    required: false
    type: int
  vlans:
    description:
    - Only used with shared connection. VLANs to attach. Pass one vlan for Primary/Single
      connection and two vlans for Redundant connection
    elements: int
    required: false
    type: list
  vrfs:
    description:
    - List of connection ports - primary (`ports[0]`) and secondary (`ports[1]`)
    elements: str
    required: false
    type: list
requirements: null
short_description: Manage a interconnection in Equinix Metal
'''
EXAMPLES = '''
- name: Create new connection
  hosts: localhost
  tasks:
  - equinix.cloud.metal_connection:
      project_id: Bhf47603-7a09-4ca1-af67-4087c13ab5b6
      name: new connection
      type: dedicated
      redundancy: primary
      speed: 50Mbps
      metro: am
'''
RETURN = '''
metal_resource:
  description: The module object
  returned: always
  sample:
  - "\n{\n    \"project_id\": \"Bhf47603-7a09-4ca1-af67-4087c13ab5b6\"\n    \"name\"\
    : \"new connection\"\n    \"type\": \"dedicated\"\n    \"redundancy\": \"primary\"\
    \n    \"speed\": \"50Mbps\"\n    \"metro\": \"am\"\n}\n"
  type: dict
'''

# End of generated documentation

# This is a template for a new module. It is not meant to be used as is.
# It is meant to be copied and modified to create a new module.
# Replace all occurrences of "metal_resource" with the name of the new
# module, for example "metal_vlan".


from ansible.module_utils._text import to_native
from ansible_specdoc.objects import (
    SpecField,
    FieldType,
    SpecReturnValue,
)
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
    getSpecDocMeta,
)

MEGA = 1000 * 1000
GIGA = 1000 * MEGA
allowed_speeds = [
    (50 * MEGA, "50Mbps"),
    (200 * MEGA, "200Mbps"),
    (500 * MEGA, "500Mbps"),
    (1 * GIGA, "1Gbps"),
    (2 * GIGA, "2Gbps"),
    (5 * GIGA, "5Gbps"),
    (10 * GIGA, "10Gbps"),
]
MODULE_NAME = "metal_connection"

module_spec = dict(
    id=SpecField(
        type=FieldType.string,
        description=["UUID of the connection."],
    ),
    connection_id=SpecField(
        type=FieldType.string,
        description=["UUID of the connection, used for GET."],
    ),
    project_id=SpecField(
        type=FieldType.string,
        description=["UUID of the project this connection belongs to."],
    ),
    organization_id=SpecField(
        type=FieldType.string,
        description=["UUID of the organization this connection belongs to."],
    ),
    contact_email=SpecField(
        type=FieldType.string,
        description=["Email for the person to contact for inquires."],
        editable=True,
    ),
    description=SpecField(
        type=FieldType.string,
        description=["Description of the connection."],
        editable=True,
    ),
    metro=SpecField(
        type=FieldType.string,
        description=["Metro where the connection will be created"],
    ),
    mode=SpecField(
        type=FieldType.string,
        description=["Mode for connections in IBX facilities with the dedicated type - standard or tunnel"],
        editable=True,
        choices=["standard", "tunnel"]
    ),
    name=SpecField(
        type=FieldType.string,
        description=["Name of the connection resource"],
        editable=True,
    ),
    redundancy=SpecField(
        type=FieldType.string,
        description=["Connection redundancy - redundant or primary"],
        editable=True,
        choices=["redundant", "primary"]
    ),
    service_token_type=SpecField(
        type=FieldType.string,
        description=["Only used with shared connection. Type of service token to use for the connection, a_side or z_side"],
        choices=["a_side", "z_side"]
    ),
    speed=SpecField(
        type=FieldType.string,
        description=[f"Port speed. Required for a_side connections. Allowed values are {[s[1] for s in allowed_speeds]}"],
    ),
    tags=SpecField(
        type=FieldType.list,
        description=["Tags attached to the connection"],
        editable=True,
        element_type=FieldType.string,
    ),
    type=SpecField(
        type=FieldType.string,
        description=["Connection type - dedicated or shared"],
        choices=["dedicated", "shared"]
    ),
    vlans=SpecField(
        type=FieldType.list,
        description=["Only used with shared connection. VLANs to attach. Pass one vlan for Primary/Single connection and two vlans for Redundant connection"],
        element_type=FieldType.integer,
    ),
    vrfs=SpecField(
        type=FieldType.list,
        description=["List of connection ports - primary (`ports[0]`) and secondary (`ports[1]`)"],
        element_type=FieldType.string,
    ),
)


specdoc_examples = [
    """
- name: Create new connection
  hosts: localhost
  tasks:
  - equinix.cloud.metal_connection:
      project_id: "Bhf47603-7a09-4ca1-af67-4087c13ab5b6"
      name: "new connection"
      type: "dedicated"
      redundancy: "primary"
      speed: "50Mbps"
      metro: "am"
""",
]

result_sample = [
    """
{
    "project_id": "Bhf47603-7a09-4ca1-af67-4087c13ab5b6"
    "name": "new connection"
    "type": "dedicated"
    "redundancy": "primary"
    "speed": "50Mbps"
    "metro": "am"
}
"""
]

MUTABLE_ATTRIBUTES = [k for k, v in module_spec.items() if v.editable]

SPECDOC_META = getSpecDocMeta(
    short_description="Manage a interconnection in Equinix Metal",
    description=(
        "Manage the interconnection in Equinix Metal. "
        "You can use *id* or *name* to lookup the resource. "
        "If you want to create new resource, you must provide *project_id*, *name*, *type*, *redundancy* and *speed*."
    ),
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "metal_resource": SpecReturnValue(
            description="The module object",
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        required_one_of=[("name", "id", "connection_id"), ("project_id", "organization_id")],
    )

    vlans = module.params.get("vlans") 
    connection_type = module.params.get("type")

    if connection_type == "dedicated":
        if vlans:
          module.fail_json(msg="A 'dedicated' connection can't have vlans.")
        if module.params.get("service_token_type"):
          module.fail_json(msg="A 'dedicated' connection can't have a set service_token_type.")
    elif connection_type == "shared":
        if not module.params.get("project_id"):
          module.fail_json(msg="You must provide 'project_id' for a 'shared' connection.")
        if module.params.get("mode") == "tunnel":
          module.fail_json(msg="A 'shared' connection doesn't support 'tunnel' mode.")
        if module.params.get("redundancy") == "primary" and len(vlans > 1):
          module.fail_json(msg="A 'shared' connection without redundancy can only have 1 vlan.")
        if not module.params.get("service_token_type"):
          module.fail_json(msg="A 'shared' connection must have a set service_token_type.")

    if module.params.get("speed"):
        module.params["speed"] = speed_str_to_int(module)

    state = module.params.get("state")
    changed = False

    try:
        module.params_syntax_check()
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id(MODULE_NAME, tolerate_not_found)
        else:
            fetched = module.get_one_from_list(
                MODULE_NAME,
                ["name"],
            )

        if fetched:
            module.params["id"] = fetched["id"]
            if state == "present":
                diff = get_diff(module.params, fetched, MUTABLE_ATTRIBUTES)
                if diff:
                    fetched = module.update_by_id(diff, MODULE_NAME)
                    changed = True

            else:
                module.delete_by_id(MODULE_NAME)
                changed = True
        else:
            if state == "present":
                fetched = module.create(MODULE_NAME)
                if "id" not in fetched:
                    module.fail_json(msg=f"UUID not found in {MODULE_NAME} creation response")
                changed = True
            else:
                fetched = {}
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg=f"Error in {MODULE_NAME}: {to_native(e)}", exception=tb)

    fetched.update({"changed": changed})
    module.exit_json(**fetched)


def speed_str_to_int(module):
    raw_speed = module.params["speed"]

    for speed, speed_str in allowed_speeds:
        if raw_speed == speed_str:
            return speed
    raise module.fail_json(msg=f"Speed value invalid, allowed values are {[s[1] for s in allowed_speeds]}")


if __name__ == "__main__":
    main()
