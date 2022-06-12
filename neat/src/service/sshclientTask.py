import celery


# TODO client超时自动关闭
from neat.src.app.moudles import Server
from neat.src.service.sshclient import SshClient


class SshClientTask(celery.Task):
    autoretry_for = (Exception,)
    max_retries = 3
    # exponential backoff
    retry_backoff = True
    # sec
    retry_backoff_max = 20
    # 默认为True,若 full_jitter 是 False，则不是随机选取，
    # 而是取最大的补偿时间，也就可能导致多个任务同时再次执行
    retry_jitter = True
    serializer = 'pickle'

    _client_dict = {}

    def __get_sshclient(self, host, port, user, password):
        client = SshClient(host, port, user, password)
        return client

    def client(self, server: Server):
        if self._client_dict.get(server.ip) is None:
            self._client_dict[server.ip] = self._get_sshclient(server.ip, server.port, server.user,
                                                               server.password)
        return self._client_dict.get(server.ip)
