import paramiko
import subprocess
import pytest

# Server details (update these with actual credentials)
server_ip = '127.0.0.1'
username = 'dymytryke'
password = '1234qwer'

@pytest.fixture(scope='function')
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Connect to the server
        ssh.connect(server_ip, username=username, password=password)
        # Start the iperf server
        stdin, stdout, stderr = ssh.exec_command("iperf -s")
        # Allow some time for the server to start
        yield stdout.read().decode(), stderr.read().decode()
    finally:
        # Stop the iperf server and close the connection
        ssh.exec_command("pkill iperf")
        ssh.close()

@pytest.fixture(scope='function')
def client(server):
    try:
        # Run the iperf client
        command = ["iperf", "-c", server_ip, "-i", "1"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode(), error.decode()
    except Exception as e:
        return "", str(e)
