import paramiko
import subprocess
import pytest

# Дані вашого серверу, які будуть використовуватися для підключення по ssh до серверу. підняття iperf сервера
server_ip = '3.14.10.7'
username = 'ubuntu'
rsa_key_file = "/home/madgicx/.ssh/embedded.pem"


@pytest.fixture(scope='function')
def server():

    command = "iperf3 -s --one-off"

    server_ = paramiko.SSHClient()
    key_ = paramiko.RSAKey.from_private_key_file(rsa_key_file)
    server_.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    server_.connect(hostname='ec2-3-14-10-7.us-east-2.compute.amazonaws.com',
                    username=username,
                    pkey=key_,
                    look_for_keys=False,
                    allow_agent=False)
    _, _, error = server_.exec_command(command)
    server_.close()
    return error.read()


@pytest.fixture(scope='function')
def client(server):

    process = subprocess.Popen(['iperf3', '-c', server_ip, '-i', '2'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = process.communicate()
    return stdout, stderr, server
