# Copyright 2016: Intel Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import jsonschema
import random

from rally.common import logging
from rally import consts
from rally import exceptions as rally_exceptions
from rally.plugins.openstack import scenario
from rally.plugins.openstack.scenarios.cinder import utils as cinder_utils
from rally.plugins.openstack.scenarios.nova import utils
from rally.plugins.openstack.wrappers import network as network_wrapper
from rally.task import types
from rally.task import utils as task_utils
from rally.task import validation
from rally.task import atomic


class NovaLiveMigrations(utils.NovaScenario):
    """Plugin for Live Migration specific scenarios"""

    def _get_random_server(self):
        """Returns random server from existing ones"""
#        import pdb; pdb.set_trace()
        servers = self._list_servers()
        return random.choice(servers)



    @types.convert(image={"type": "glance_image"},
                   flavor={"type": "nova_flavor"})
    @validation.image_valid_on_flavor("flavor", "image")
    @validation.required_services(consts.Service.NOVA)
    @validation.required_openstack(admin=True, users=True)
    @scenario.configure()
    @atomic.action_timer("get_and_live_migrate_random_server")
    def get_and_live_migrate_random_server(self, image,
                                     flavor, block_migration=False,
                                     disk_over_commit=False, min_sleep=0,
                                     max_sleep=0, **kwargs):
        """Live Migrate a server.
        This scenario launches a VM on a compute node available in
        the availability zone and then migrates the VM to another
        compute node on the same availability zone.
        Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
        to simulate a pause between VM booting and running live migration
        (of random duration from range [min_sleep, max_sleep]).
        :param image: image to be used to boot an instance
        :param flavor: flavor to be used to boot an instance
        :param block_migration: Specifies the migration type
        :param disk_over_commit: Specifies whether to allow overcommit
                                 on migrated instance or not
        :param min_sleep: Minimum sleep time in seconds (non-negative)
        :param max_sleep: Maximum sleep time in seconds (non-negative)
        :param kwargs: Optional additional arguments for server creation
        """
        server = self._get_random_server()
        self.sleep_between(min_sleep, max_sleep)

        new_host = self._find_host_to_migrate(server)
        self._live_migrate(server, new_host,
                           block_migration, disk_over_commit)
