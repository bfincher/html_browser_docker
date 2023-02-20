#!/usr/bin/python3

import pickle
import re
import socket
import sys

DEFAULT_LISTEN_HOST = '0.0.0.0'
DEFAULT_LISTEN_PORT = 5000
DEFAULT_NGINX_CONFIG_FILE = '/etc/nginx/conf.d/default.conf'

REGEX = re.compile(r'location download_([a-zA-Z_0-9-]+)\s+{')

class DynamicUpdate:
    def __init__(self, listen_host, listen_port, nginx_config_file):
        self.shares = []
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.nginx_config_file = nginx_config_file

    def loadConfig(self):
        with open(self.nginx_config_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            match = REGEX.match(line)
            if match:
                self.shares.append(match.group(1))

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.listen_host, self.listen_port))
            while True:
                s.listen()
                conn, addr = s.accept()
                print(f'Connected to {addr}')

                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.handle_new_share(data)

    def handle_new_share(self, dataStr):
        data = pickle.loads(dataStr)
        for item in data:
            print(f'item = {item}')

def create_instance_from_args(args = None):
    listen_host = DEFAULT_LISTEN_HOST
    listen_port = DEFAULT_LISTEN_PORT
    nginx_config_file = DEFAULT_NGINX_CONFIG_FILE

    if args:
        i = 1
        while i < len(args):
            arg = args[i]
            if arg == '--listen-host':
                i += 1
                listen_host = args[i]
            elif arg == '--listen-port':
                i += 1
                listen_port = int(args[i])
            elif arg == '--nginx-config-file':
                i += 1
                nginx_config_file = args[i]
            else:
                raise Exception(f"Invalid argument: {arg}")
            i += 1

    du = DynamicUpdate(listen_host, listen_port, nginx_config_file)
    return du

if __name__ == '__main__':
    instance = create_instance_from_args(sys.argv)
    instance.loadConfig()
    instance.listen()
