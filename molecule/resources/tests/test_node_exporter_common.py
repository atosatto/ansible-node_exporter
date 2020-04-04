import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_node_exporter_service(host):

    s = host.service('node_exporter')
    assert s.is_running
    assert s.is_enabled


def test_node_exporter_webserver(host):

    host.socket("tcp://127.0.0.1:9100").is_listening
