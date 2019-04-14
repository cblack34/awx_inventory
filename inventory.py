#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class HostDoesNotExist(Exception):
    """Used when trying to use a host that does not exist."""
    pass


class HostAlreadyExist(Exception):
    """Used when trying to add a host that already exist"""
    pass


class GroupAlreadyExist(Exception):
    """Used when trying to add a group that already exist."""
    pass


class GroupDoesNotExist(Exception):
    """Used when trying to use a group that does not exist."""


class AwxInventory:
    """Inventory for Ansible and AWX.

    Allows the creation of inventories to be used with Ansible.
    Can be used with any dict encoder that has a dumps method. see export method.
    """

    def __init__(self):
        self.hosts = {}
        self.groups = {}

    def add_host(self, name, host_vars=None, groups=None):
        """Add a vm to inventory, Optionally add vars to that vm, and
           Optionally add groups to that vm.

           If groups are provided this function will create the group if it does not exist and
           then add the vm to the group.

        Arguments:
            name   {str}     -- ID of the VM in source api. In vmware this would look like: vm-143230
            vars    {dict}    -- Vars that should be added to this vm.
            groups  {list}    -- Groups this vm is a member of.
        """
        if name in self.hosts:
            raise HostAlreadyExist

        self.hosts[name] = {}

        if host_vars != None:
            self.add_host_vars(name, host_vars)

        if groups != None:
            for group in groups:
                try:
                    self.groups[group]
                except KeyError:
                    self.add_group(group)

                self.add_host_to_group(name, group)

    def remove_host(self, host_name):
        """Remove a vm from the inventory.

        Arguments:
            host_name {str} -- ID of the VM in source api. In vmware this would look like: vm-143230
        """

        # Remove host from hosts list.
        try:
            self.hosts.pop(host_name)
        except KeyError:
            pass

        # Remove host from all groups
        for k, v in self.groups.items():
            try:
                self.groups[k]['hosts'].remove(host_name)
            except KeyError:
                pass

    def add_group(self, name, group_vars=None, hosts=None):
        """Add a group to inventory, Optionally add group vars, and Optionally add hosts of the group.

        Arguments:
            name {str} -- Name of the group
            vars {dict} -- Vars that should be added to this group
            hosts {list} -- VMs that should be added to this group.
        """
        if name in self.groups:
            raise GroupAlreadyExist

        self.groups[name] = {}

        if group_vars != None:
            self.add_group_vars(name, group_vars)

        if hosts != None:
            for host in hosts:
                self.add_host_to_group(host, name)

    def add_host_vars(self, name, host_vars):
        """Add vars to an existing name.
           This will over write vars with matching keys.

        Arguments:
            :type name: str         -- ID of the VM in source api. In vmware this would look like: name-143230
            :type host_vars: dict   -- Vars that should be added to this name.
        """
        # Make sure host exist
        try:
            self.hosts[name]
        except KeyError:
            raise HostDoesNotExist


        # Patch the keys in host vars
        for k, v in host_vars.items():
            self.hosts[name][k] = v

    def add_group_vars(self, group, group_vars):
        """Add vars to an existing group.
           This will over write vars with matching keys.

        Arguments:
            :type group: str -- Name of group in inventory
            :type group_vars: dict -- Vars that should be added to this group.
        """
        # Make sure the group exist
        try:
            self.groups[group]

        except KeyError:
            raise GroupDoesNotExist

        # Make sure the group has the vars key
        try:
            self.groups[group]['vars']
        except KeyError:
            self.groups[group]['vars'] = {}

        # Patch the keys in group vars
        for k, v in group_vars.items():
            self.groups[group]['vars'][k] = v

    def add_host_to_group(self, host, group):
        """Add host to group.

        Arguments:
            host {str}    -- ID of the VM in source api. In vmware this would look like: host-143230
            group {str} -- Name of group in inventory
        """
        # Make sure host exist
        try:
            self.hosts[host]
        except KeyError:
            raise HostDoesNotExist

        # Make sure group exist
        try:
            self.groups[group]
        except KeyError:
            raise GroupDoesNotExist

        # Make sure group has hosts key
        try:
            self.groups[group]['hosts']
        except KeyError:
            self.groups[group]['hosts'] = []

        self.groups[group]['hosts'].append(host)

    def export(self, encoder=json):
        """Convert from object to string using the dumps method of the encoder class.

        Keyword Arguments:
            encoder {module} -- Class to encode dict to output string. (default: {json})
        """

        # dict that will be dumped to screen.
        awx_inv = {}


        # Add 'all' group and add all host to group.
        self.add_group('all')
        for k, v in self.hosts.items():
            self.add_host_to_group(k, 'all')

        # Add non-empty groups to export.
        for group in self.groups:
            if len(self.groups[group]) > 0:
                awx_inv[group] = self.groups[group]

        awx_inv['_meta'] = {}
        awx_inv['_meta']['hostvars'] = self.hosts

        return encoder.dumps(awx_inv, indent=2)
