# !/usr/bin/env python

# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from utils import read_json_from_file
import re

class Role():

    def __init__(self, role, ossec_path):
        self.role = role
        self._load_role_permissions_from_file(ossec_path)

    def __str__(self):
        return self.role

    def _load_role_permissions_from_file(self, ossec_path):
        roles_mapping = read_json_from_file(ossec_path + "/api/models/rbac/roles_mapping.json")

        self.permissions = roles_mapping.get(self.role)
        if not self.permissions:
            raise Exception("No mapping found for role `{}`".format(self.role))

    def can_exec(self, request_method, request_resource):
        can_exec_request = False
        for role_resource, permissions_for_resource in self.permissions.items():
            # Check resource
            if "*" in role_resource:
                role_resource = role_resource.replace('*', ".*")

            regex = re.compile(r'^' + role_resource + '$')
            if not regex.match(request_resource):
                continue

            # Check method
            can_exec_request = True if permissions_for_resource['methods'] == "*" \
                else request_method in permissions_for_resource['methods']
            if can_exec_request:
                break

        return can_exec_request
