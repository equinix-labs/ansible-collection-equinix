# metal_virtual_circuit_info

Gather information about Equinix Metal Virtual Circuits


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all projects in an organization
  hosts: localhost
  tasks:
      - equinix.cloud.metal_virtual_circuit_info:
          organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `connection_id` | <center>`str`</center> | <center>Optional</center> | ID of the virtual circuit resource   |
| `organization_id` | <center>`str`</center> | <center>Optional</center> | ID of the organisation to which the virtual circuit belongs   |






## Return Values



### Sample Response for resources
```json
{
  "backend_transfer_enabled": false,
  "customdata": {},
  "description": "",
  "id": "31d3ae8b-bd5a-41f3-a420-055211345cc7",
  "name": "ansible-integration-test-project-csle6t2y-project2",
  "organization_id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
  "payment_method_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
}
```


