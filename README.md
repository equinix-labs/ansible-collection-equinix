# Equinix Ansible Collection
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-equinix.cloud-660198.svg?style=flat)](https://galaxy.ansible.com/equinix/cloud/) 
![Tests](https://img.shields.io/github/actions/workflow/status/equinix-labs/ansible-collection-equinix/integration-tests.yml?branch=main)

The Ansible Collection Equinix contains various plugins for managing Equinix services.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible version **6.7.0**, core version **2.13.8**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

<!--start collection content-->
### Modules

Modules for managing Equinix infrastructure.

Name | Description |
--- | ------------ |
[equinix.cloud.metal_device](./docs/modules/metal_device.md)|Create, update, or delete Equinix Metal devices|
[equinix.cloud.metal_ip_assignment](./docs/modules/metal_ip_assignment.md)|Manage Equinix Metal IP assignments|
[equinix.cloud.metal_project](./docs/modules/metal_project.md)|Manage Projects in Equinix Metal|
[equinix.cloud.metal_reserved_ip_block](./docs/modules/metal_reserved_ip_block.md)|Create/delete blocks of reserved IP addresses in a project.|


### List Modules

Modules for retrieving information about existing Equinix infrastructure. Output of these modules is always a list.

Name | Description |
--- | ------------ |
[equinix.cloud.metal_available_ips_list](./docs/modules/metal_available_ips_list.md)|Get list of avialable IP addresses from a reserved IP block|
[equinix.cloud.metal_device_list](./docs/modules/metal_device_list.md)|Select list of Equinix Metal devices|
[equinix.cloud.metal_ip_assignment_list](./docs/modules/metal_ip_assignment_list.md)|Gather IP address assignments for a device|
[equinix.cloud.metal_project_list](./docs/modules/metal_project_list.md)|Gather information about Equinix Metal projects|
[equinix.cloud.metal_reserved_ip_block_list](./docs/modules/metal_reserved_ip_block_list.md)|Gather list of reserved IP blocks|


### Inventory Plugins

Dynamically add Equinix infrastructure to an Ansible inventory.

Name |
--- |
[equinix.cloud.metal_device](./docs/inventory/metal_device.rst)|


<!--end collection content-->

## Installation

You can install the Equinix collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install equinix.cloud
```

The Python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```shell
pip install -r https://raw.githubusercontent.com/equinix-labs/ansible-collection-equinix/main/requirements.txt
```

## Usage
Once the Equinix Ansible collection is installed, it can be referenced by its [Fully Qualified Collection Namespace (FQCN)](https://github.com/ansible-collections/overview#terminology): `equinix.cloud.module_name`.

In order to use this collection, you should have account in the relevant Equinix service. For example you should have an account in Equinix Metal to use the `metal_*` modules.

You can authenticate either by exporting auth token in an environment variable, or by supplying `*_api_token` attributes to modules. For example, to use `metal_device`, you can export `METAL_AUTH_TOKEN` (or `METAL_API_TOKEN`), or you can supply the `metal_api_token` attribute.

### Example Playbook

```yaml
---
- name: create Equinix Metal device
  hosts: localhost
  tasks:
    - equinix.cloud.metal_device:
        project_id: "3b516842-c8b1-485e-9f76-c891bd804c5e"
        hostname: "my new device"
        operating_system: ubuntu_20_04
        plan: c3.small.x86
        metro: sv
```

For more information on Ansible collection usage, see [Ansible's official usage guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## Examples

Use-case examples for this collection can be found [here](./examples).

## Development

If you want to develop the collecton, it's best to clone it under directory tree `ansible_collections/equinix/cloud`. That way the integration tests can be run without actually installing.

```
git clone https://github.com/equinix-labs/ansible-collection-equinix devdir/ansible_collections/equinix/cloud
```

You can try to run integration test for metal_project, that won't incur any fee.

```
cd devdir/ansible_collections/equinix/cloud
ansible-test integration -vvv metal_project
```

You can then edit existing code, or add new modules or tests.

To install the collection from local directory, do `make install` in the root of the repo.



## Releasing

Go to [https://github.com/equinix-labs/ansible-collection-equinix/releases/new](https://github.com/ansible-collection-equinix/metal-python/releases/new) and create a new release from `main`. Don't choose an existing tag. Put version to the field for "Release title", for example `v0.1.2`. Don't add collection number to the Makefile.

Add release notes in format of [Terraform Provider Equinix](https://github.com/equinix/terraform-provider-equinix/releases), with at least one of the sections (NOTES, FEATURES, BUG FIXES, ENHANCEMENTS).

Click "Publish release", and the manual part should be over.

The release will create a tag, and we have a Github action in place that should create an Ansible Galaxy release. The script that creates tarball for Galay removes the first "v", so releasing `v0.1.2` should upload collection equinix.cloud version 0.1.2.

Verify that the [releasing Github action](https://github.com/equinix-labs/ansible-collection-equinix/actions) succeeded.

Verify that new version of [equinix.cloud](https://galaxy.ansible.com/equinix/cloud) is available in Ansible Galaxy.


## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.