# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

try:
    import metal_python
except ImportError:
    # This is handled in raise_if_missing_metal_python()
    pass

from ansible_collections.equinix.cloud.plugins.module_utils import (
    action,
    utils,
)

from ansible_collections.equinix.cloud.plugins.module_utils.metal import (
    metal_client,
    spec_types,
)


def build_api_call(specs: spec_types.Specs, params: dict):
    return spec_types.ApiCall(specs, params)


def get_routes(mpc):
    """
    This function returns a dictionary of API call configurations.
    """

    # we check for the presence of the metal_python module here, because
    # the ApiCallConfigs use classes straight from the metal_python module
    # and we prefer to fail early and hopefully into module.fail_json()
    metal_client.raise_if_missing_metal_python()

    return {
        # GETTERS
        ('metal_device', action.GET): spec_types.Specs(
            metal_python.DevicesApi(mpc).find_device_by_id,
            ),
        ('metal_project', action.GET): spec_types.Specs(
            metal_python.ProjectsApi(mpc).find_project_by_id,
            ),
        ('metal_ip_reservation', action.GET): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).find_ip_address_by_id,
        ),
        ('metal_ip_assignment', action.GET): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).find_ip_address_by_id,
        ),

        # LISTERS
        ('metal_project_device', action.LIST): spec_types.Specs(
            metal_python.DevicesApi(mpc).find_project_devices,
            {'id': 'project_id'},
        ),
        ('metal_organization_device', action.LIST): spec_types.Specs(
            metal_python.DevicesApi(mpc).find_organization_devices,
            {'id': 'organization_id'},
            ),
        ('metal_project', action.LIST): spec_types.Specs(
            metal_python.ProjectsApi(mpc).find_projects,
        ),
        ('metal_organization_project', action.LIST): spec_types.Specs(
            metal_python.OrganizationsApi(mpc).find_organization_projects,
            {'id': 'organization_id'},
        ),
        ('metal_ip_reservation', action.LIST): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).find_ip_reservations,
            {'id': 'project_id'},
        ),
        ('metal_available_ip', action.LIST): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).find_ip_availabilities,
            {'id': 'reserved_ip_block_id'},
        ),
        ('metal_ip_assignment', action.LIST): spec_types.Specs(
            metal_python.DevicesApi(mpc).find_ip_assignments,
            {'id': 'device_id'}
        ),

        # DELETERS
        ('metal_device', action.DELETE): spec_types.Specs(
            metal_python.DevicesApi(mpc).delete_device,
            ),
        ('metal_project', action.DELETE): spec_types.Specs(
            metal_python.ProjectsApi(mpc).delete_project,
            ),
        ('metal_ip_reservation', action.DELETE): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).delete_ip_address,
        ),
        ('metal_ip_assignment', action.DELETE): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).delete_ip_address,
        ),


        # CREATORS
        ('metal_device_metro', action.CREATE): spec_types.Specs(
            metal_python.DevicesApi(mpc).create_device,
            {'id': 'project_id'},
            metal_python.CreateDeviceRequest,
            ),
        ('metal_device_facility', action.CREATE): spec_types.Specs(
            metal_python.DevicesApi(mpc).create_device,
            {'id': 'project_id'},
            metal_python.CreateDeviceRequest,
        ),
        ('metal_project', action.CREATE): spec_types.Specs(
            metal_python.ProjectsApi(mpc).create_project,
            {},
            metal_python.ProjectCreateFromRootInput,
        ),
        ('metal_organization_project', action.CREATE): spec_types.Specs(
            metal_python.OrganizationsApi(mpc).create_organization_project,
            {'id': 'organization_id'},
            metal_python.ProjectCreateInput,
            ),
        ('metal_ip_reservation', action.CREATE): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).request_ip_reservation,
            {'id': 'project_id'},
            metal_python.models.RequestIPReservationRequest,
        ),
        ('metal_ip_assignment', action.CREATE): spec_types.Specs(
            metal_python.DevicesApi(mpc).create_ip_assignment,
            {'id': 'device_id'},
            metal_python.models.IPAssignmentInput,
        ),

        # UPDATERS
        ('metal_device', action.UPDATE): spec_types.Specs(
            metal_python.DevicesApi(mpc).update_device,
            {},
            metal_python.DeviceUpdateInput,
        ),
        ('metal_project', action.UPDATE): spec_types.Specs(
            metal_python.ProjectsApi(mpc).update_project,
            {},
            metal_python.ProjectUpdateInput,
        ),
        ('metal_ip_reservation', action.UPDATE): spec_types.Specs(
            metal_python.IPAddressesApi(mpc).update_ip_address,
            {},
            metal_python.models.IPAssignmentUpdateInput,
        ),
    }