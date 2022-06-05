import paramiko
from scp import SCPClient


class SshClient(object):

    def __init__(self, host, port, user, password, timeout=10):
        self.client = paramiko.SSHClient()
        self.host = host
        self.timeout = timeout
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f'connected {host}')
        self.client.connect(hostname=host, port=port, username=user, password=password,
                            timeout=timeout)

    def command(self, cmd_command):
        stdin, stdout, stderr = self.client.exec_command(cmd_command)
        stderr_print = stderr.read()
        stdout_print = str(stdout.read(), 'utf-8')
        channel = stdout.channel
        status = channel.recv_exit_status()
        print(f"[{self.host}]-exit_status: {status}")
        if len(stderr_print) > 0:
            print(f"[{self.host}]-stderr: {stderr_print.decode()}")
        if len(stdout_print) > 0:
            print(f"########### [{self.host}]-stdout ###########\n {stdout_print}")
        return status

    def scp(self, local_path, remote_path):
        scpclient = SCPClient(self.client.get_transport(), socket_timeout=self.timeout)
        try:
            scpclient.put(local_path, remote_path)
        except FileNotFoundError as e:
            print(e)
            print("System not found such file:" + local_path)
        else:
            print(f"{local_path} upload to {self.host}:{remote_path}")

    def close(self):
        self.client.close()