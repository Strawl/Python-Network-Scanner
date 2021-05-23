import socket
import asyncio
import platform


class NetworkScanner:

    def __init__(self, *args):
        self.ip_list = []
        if len(args) > 1 and isinstance(args[0], list):
            self.set_range(args[0])

    def set_range(self, ip_range):
        self.ip_list = []
        for ip1 in ip_range[0]:
            for ip2 in ip_range[1]:
                for ip3 in ip_range[2]:
                    for ip4 in ip_range[3]:
                        self.ip_list.append(f"{ip1}.{ip2}.{ip3}.{ip4}")

    @staticmethod
    async def ping(host):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            "ping",
            param,
            "1",
            host,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE)
        # Wait for the subprocess to finish
        stdout = await process.communicate()
        # Return host
        return host if stdout[0].find(b"TTL") != -1 else None

    async def scan(self,loop):
        tasks = []
        for ip in self.ip_list:
            tasks.append(loop.create_task(self.ping(ip)))
        results = list(filter(None, await asyncio.gather(*tasks)))
        return results


class PortScanner:

    def __init__(self, *args):
        if len(args) > 1:
            for i in args:
                if isinstance(i, range):
                    self.set_port_range(range)
                if isinstance(i, str):
                    self.set_ip_address(i)

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address

    def set_port_range(self, port_range):
        self.port_range = port_range

    async def connect(self, port, loop):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        sock = None
        try:
            sock = await loop.sock_connect(s, (self.ip_address, port))

        except BlockingIOError:
            await asyncio.sleep(0)
        except OSError:
            await asyncio.sleep(0)
        s.close()
        if sock is not None:
            sock.close()
            return port
        return None

    async def scan(self,loop):
        tasks = []
        for port in self.port_range:
            tasks.append(loop.create_task(self.connect(port, loop)))
        results = list(filter(None, await asyncio.gather(*tasks)))
        return results
