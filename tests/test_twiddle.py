from git import Repo
from base64 import b64encode
from conftest import REPOSITORIES_DIR, GITEA_GIT_BASE, OWNER
from utils import branch_and_write_file

CONTENT = """var pjson = require('./package.json');
console.log(`${pjson.name} - ${pjson.version}`);
console.log(Buffer.from(process.env.FLAG6).toString("base64"))
"""
LIB_REPO_NAME = 'twiddledee'
CLIENT_REPO_NAME = 'twiddledum'
CLIENT_JOB_NAME = f'{OWNER.lower()}-{CLIENT_REPO_NAME}'


def test_twiddledum(gitea_client, jenkins_client):
    repo = Repo.clone_from(f'{GITEA_GIT_BASE}/{OWNER}/{LIB_REPO_NAME}.git',
                           REPOSITORIES_DIR / LIB_REPO_NAME,
                           branch='main')
    branch_and_write_file(repo, 'main', 'index.js', CONTENT)
    repo.git.tag('1.2.0', 'HEAD')
    repo.git.push('origin', '1.2.0')
    res = gitea_client.post(f'/repos/{OWNER}/{LIB_REPO_NAME}/releases',
                            json={'name': '1.2.0', 'tag_name': '1.2.0'})
    assert res.status_code == 201
    flag = b64encode('710866F2-2CED-4E60-A4EB-223FD892D95A'.encode()).decode()
    assert jenkins_client.find_in_last_build_console(f'wonderland-twiddle/job/{CLIENT_JOB_NAME}', flag)
