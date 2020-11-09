import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("name", ["strongswan", "monit"])
def test_packages(host, name):
    pkg = host.package(name)

    assert pkg.is_installed


@pytest.mark.parametrize("path,user,group", [
    ("/etc/hosts", "root", "root"),
    ("/etc/ipsec.conf", "root", "root"),
    ("/etc/monit/conf.d/ipsec", "root", "root"),
])
def test_files(host, path, user, group):
    f = host.file(path)

    assert f.exists
    assert f.user == user
    assert f.group == group


@pytest.mark.parametrize("name", ["ipsec", "monit"])
def test_services(host, name):
    service = host.service(name)

    assert service.is_running


def test_monit_ipsec_conf_file(host):
    f = host.file("/etc/monit/conf.d/ipsec")
    expected_content_string = """check host ipsec_test with address 8.8.8.8
    start program = "/etc/init.d/ipsec start"
    stop program = "/etc/init.d/ipsec stop"
    if failed ping then restart
    if 3 restarts within 3 cycles then exec /etc/monit/exec-scripts/opsgenie-notification\n\n"""  # noqa: E501
    assert f.content_string == expected_content_string
