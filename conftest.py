import pytest
import paramiko
import subprocess

# Server details (to be filled with the server's credentials)
SERVER_IP = '127.0.0.1'
USERNAME = 'dymytryke'
PASSWORD = '1234qwer'

@pytest.fixture(scope='function')
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)

    # Start iperf server
    stdin, stdout, stderr = ssh.exec_command("iperf -s")
    yield stdout.read().decode(), stderr.read().decode()

    # Stop iperf server
    ssh.exec_command("pkill iperf")
    ssh.close()


@pytest.fixture(scope='function')
def client(server):
    command = ["iperf", "-c", SERVER_IP, "-i", "1"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()
