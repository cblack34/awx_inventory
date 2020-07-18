import unittest
from unittest import TestCase

from inventory import AwxInventory


class TestAwxInventory(TestCase):

    ##########################################
    #         add_host Test
    ##########################################

    def test_add_host_creates_host_dict(self):

        inv = AwxInventory()
        inv.add_host('host1')

        self.assertIsInstance(inv.hosts, dict)

    def test_add_host_dict_value(self):

        inv = AwxInventory()
        inv.add_host('host1')

        test_dict = {
            'host1': {}
        }

        self.assertDictEqual(inv.hosts, test_dict)

    def test_add_host_with_vars(self):

        inv = AwxInventory()

        test_host_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        inv.add_host('host1', test_host_vars)

        test_dict = {
            'host1': test_host_vars
        }

        self.assertDictEqual(inv.hosts, test_dict)

    def test_add_host_with_groups_creates_group_dict(self):

        inv = AwxInventory()

        test_groups = [
            'group1'
        ]

        inv.add_host('host1', groups=test_groups)

        self.assertIsInstance(inv.groups, dict)

    def test_add_host_with_groups_creates_group_dict_values(self):

        inv = AwxInventory()

        test_groups = [
            'group1'
        ]

        inv.add_host('host1', groups=test_groups)

        test_dict = {
            'group1': {
                'hosts': [
                    'host1'
                ]
            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    def test_add_host_with_vars_and_groups_dict_values_group(self):

        inv = AwxInventory()

        test_groups = [
            'group1'
        ]

        test_host_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        inv.add_host('host1', host_vars=test_host_vars, groups=test_groups)

        test_group_dict = {
            'group1': {
                'hosts': [
                    'host1'
                ]
            }
        }

        self.assertDictEqual(inv.groups, test_group_dict)

    def test_add_host_with_vars_and_groups_dict_values_host(self):

        inv = AwxInventory()

        test_groups = [
            'group1'
        ]

        test_host_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        inv.add_host('host1', host_vars=test_host_vars, groups=test_groups)

        test_host_dict = {
            'host1': test_host_vars
        }

        self.assertDictEqual(inv.hosts, test_host_dict)

    def test_add_host_that_already_exist_raises_exception(self):
        from inventory import HostAlreadyExist

        inv = AwxInventory()
        inv.add_host('host1')

        with self.assertRaises(HostAlreadyExist):
            inv.add_host('host1')

    ##########################################
    #         remove_host Test
    ##########################################

    def test_remove_host(self):

        inv = AwxInventory()
        inv.add_host('host1')
        inv.add_host('host2')

        inv.remove_host('host2')

        test_dict = {
            'host1': {}
        }

        self.assertDictEqual(inv.hosts, test_dict)

    def test_remove_host_from_group(self):

        inv = AwxInventory()
        inv.add_host('host1')
        inv.add_host('host2')

        inv.add_group('group1', hosts=['host1', 'host2'])

        inv.remove_host('host2')

        test_dict = {
            'group1': {
                'hosts': [
                    'host1'
                ]
            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    def test_remove_host_from_group_when_not_in_one_of_the_groups(self):

        inv = AwxInventory()
        inv.add_host('host1')
        inv.add_host('host2')

        inv.add_group('group1', hosts=['host1', 'host2'])
        inv.add_group('group2', hosts=['host1'])

        inv.remove_host('host2')

        test_dict = {
            'group1': {
                'hosts': [
                    'host1'
                ]
            },
            'group2': {
                'hosts': [
                    'host1'
                ]
            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    ##########################################
    #         add_group Test
    ##########################################

    def test_add_group_creates_dict(self):

        inv = AwxInventory()

        inv.add_group('group1')

        self.assertIsInstance(inv.groups, dict)

    def test_add_group_dict_value(self):

        inv = AwxInventory()

        inv.add_group('group1')

        test_dict = {
            'group1': {}
            }

        self.assertDictEqual(inv.groups, test_dict)

    def test_add_group_with_vars_dict_value(self):

        inv = AwxInventory()

        test_group_vars = {
            'var1': 'val1'
        }

        inv.add_group('group1', group_vars=test_group_vars)

        test_dict = {
            'group1': {
                'vars': test_group_vars
            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    def test_add_group_with_hosts(self):

        inv = AwxInventory()

        hosts = ['host1', 'host2']

        for host in hosts:
            inv.add_host(host)

        inv.add_group('group1', hosts=hosts)

        test_dict = {
            'group1': {
                'hosts': [
                    'host1',
                    'host2'
                ]
            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    def test_add_group_with_members_that_do_not_exist_raises_exception(self):
        from inventory import HostDoesNotExist

        inv = AwxInventory()

        with self.assertRaises(HostDoesNotExist):
            inv.add_group('group1', hosts=['non_existing_host'])

    def test_add_group_that_already_exist_raises_exception(self):
        from inventory import GroupAlreadyExist

        inv = AwxInventory()

        inv.add_group('group1')

        with self.assertRaises(GroupAlreadyExist):
            inv.add_group('group1')

    def test_add_group_with_members_and_vars(self):

        inv = AwxInventory()

        hosts = ['host1', 'host2']
        for host in hosts:
            inv.add_host(host)

        group_vars = {
            'var1': 'val1',
            'var2': 'val2'
        }

        inv.add_group('group1', group_vars=group_vars, hosts=hosts)

        test_dict = {
            'group1': {
                'hosts': [
                    'host1',
                    'host2'
                ],

                'vars': group_vars

            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    ##########################################
    #         add_host_vars Test
    ##########################################

    def test_add_host_vars(self):

        inv = AwxInventory()
        inv.add_host('host1')

        test_host_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        inv.add_host_vars('host1', test_host_vars)

        test_dict = {
            'host1': test_host_vars
        }

        self.assertDictEqual(inv.hosts, test_dict)

    def test_add_host_vars_replace_vars(self):

        inv = AwxInventory()
        inv.add_host('host1')

        test_host_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        inv.add_host_vars('host1', test_host_vars)

        inv.add_host_vars('host1', {'var2': 'val3'})

        test_dict = {
            'host1': {
                'var1': 'val1',
                'var2': 'val3',
            }
        }

        self.assertDictEqual(inv.hosts, test_dict)

    def test_add_host_vars_host_not_exist_raises_exception(self):
        from inventory import HostDoesNotExist

        inv = AwxInventory()

        test_host_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        with self.assertRaises(HostDoesNotExist):
            inv.add_host_vars('host1', test_host_vars)

    ##########################################
    #         add_group_vars Test
    ##########################################

    def test_add_group_vars(self):

        inv = AwxInventory()

        inv.add_group('group1')

        test_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        inv.add_group_vars('group1', test_vars)

        test_dict = {
            'group1': {
                'vars': test_vars
            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    def test_add_group_vars_group_does_not_exist_raises_exception(self):
        from inventory import GroupDoesNotExist

        inv = AwxInventory()

        test_vars = {
            'var1': 'val1',
            'var2': 'val2',
        }

        with self.assertRaises(GroupDoesNotExist):
            inv.add_group_vars('group1', test_vars)

    ##########################################
    #         remove_group Test
    ##########################################

    def test_remove_group(self):
        inv = AwxInventory()

        inv.add_group('group1')
        inv.add_group('group2')

        inv.remove_group('group1')

        test_dict = {
            'group2': {}
        }

        self.assertDictEqual(inv.groups, test_dict)

    def test_remove_group_with_host_check_hosts_host_remain(self):
        inv = AwxInventory()

        inv.add_host('host1')
        inv.add_host('host2')
        inv.add_host('host3')

        inv.add_group('group1')
        inv.add_group('group2')

        inv.add_host_to_group('host1', 'group1')
        inv.add_host_to_group('host2', 'group2')
        inv.add_host_to_group('host3', 'group1')

        inv.remove_group('group1')

        test_dict = {
            'host1': {},
            'host2': {},
            'host3': {}
        }

        self.assertDictEqual(inv.hosts, test_dict)

    def test_remove_group_with_host_check_hosts_host_removed(self):
        inv = AwxInventory()

        inv.add_host('host1')
        inv.add_host('host2')
        inv.add_host('host3')

        inv.add_group('group1')
        inv.add_group('group2')

        inv.add_host_to_group('host1', 'group1')
        inv.add_host_to_group('host2', 'group2')
        inv.add_host_to_group('host3', 'group1')

        inv.remove_group('group1', delete_host=True)

        test_dict = {
            'host2': {}
        }

        self.assertDictEqual(inv.hosts, test_dict)

    ##########################################
    #         add_host_to_group Test
    ##########################################

    def test_add_host_to_group(self):

        inv = AwxInventory()

        inv.add_host('host1')
        inv.add_group('group1')

        inv.add_host_to_group('host1', 'group1')

        test_dict = {
            'group1': {
                'hosts': [
                    'host1'
                ]
            }
        }

        self.assertDictEqual(inv.groups, test_dict)

    def test_add_host_to_group_raises_exception_no_host(self):
        from inventory import HostDoesNotExist

        inv = AwxInventory()

        inv.add_group('group1')

        with self.assertRaises(HostDoesNotExist):
            inv.add_host_to_group('host1', 'group1')

    def test_add_host_to_group_raises_exception_no_group(self):
        from inventory import GroupDoesNotExist

        inv = AwxInventory()

        inv.add_host('host1')

        with self.assertRaises(GroupDoesNotExist):
            inv.add_host_to_group('host1', 'group1')

    ##########################################
    #         export Test
    ##########################################

    # def test_export_empty(self):
    #     from inventory import AwxInventory
    #
    #     inv = AwxInventory()
    #
    #     export = inv.export()
    #
    #     self.assertDictEqual(export, {})

    # def test_export_no_host(self):
    #     from inventory import AwxInventory
    #
    #     inv = AwxInventory()
    #     inv.add_group('group1')
    #
    #     export = inv.export()
    #
    #     self.assertDictEqual(export, {})


if __name__ == '__main__':
    unittest.main()
