import os
import re
from github import Github

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

gh = Github(os.getenv('GITHUB_API_TOKEN', None))
am_last_release = re.sub('^v(.*)$', '\\1', gh.get_repo('prometheus/node_exporter').get_latest_release().tag_name)
am_last_artifact = "node_exporter-" + am_last_release + ".linux-amd64"


def test_node_exporter_binaries(host):

    amd = host.file('/usr/local/bin/node_exporter')
    assert amd.exists
    assert amd.is_symlink
    assert amd.linked_to == '/opt/' + am_last_artifact + '/node_exporter'


def test_node_exporter_release(host):

    cmd = host.run('/usr/local/bin/node_exporter --version')

    assert 'version ' + am_last_release in (cmd.stdout + cmd.stderr)
