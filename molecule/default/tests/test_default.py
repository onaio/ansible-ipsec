import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_packages(host):
    pkg = host.package("strongswan")

    assert pkg.is_installed


def test_config_file(host):
    f = host.file('/etc/ipsec.conf')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'