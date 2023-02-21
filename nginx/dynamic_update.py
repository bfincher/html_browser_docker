#!/usr/bin/python3

import pickle
import re
import socket
import sys

DEFAULT_LISTEN_HOST = '0.0.0.0'
DEFAULT_LISTEN_PORT = 5000
DEFAULT_NGINX_CONFIG_FILE = '/etc/nginx/conf.d/default.conf'

SHARE_NAME_REGEX = re.compile(r'location download_([ a-zA-Z_0-9-]+)\s+{')
SHARE_LOCATION_REGEX = re.compile(r'root\s+(.*);')

def loadConfig(config_file):
    with open(config_file, 'r') as f:
        lines = f.readlines()

    shares = {}
    for i in range(len(lines)):
        line = lines[i].strip()
        match = SHARE_NAME_REGEX.match(line)
        if match:
            share_name = match.group(1)
            i += 1
            line = lines[i].strip()
            match = SHARE_LOCATION_REGEX.match(line)
            shares[share_name] = match.group(1)
        i += 1

    return shares

class DynamicUpdate:
    def __init__(self, listen_host, listen_port, nginx_config_file):
        self.shares = {}
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.nginx_config_file = nginx_config_file

    def loadConfig(self):
        loadConfig(self.nginx_config_file)

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
        data_changed = False
        data = pickle.loads(dataStr)

        for name, location in data.items():
            if self.shares.has_key(name):
                if location != self.shares[name]:
                    self.shares[name] = location
                    data_changed = True
            else:
                self.shares[name] = location
                data_changed = True

        if data_changed:
            with open(self.nginx_config_file, 'w') as f:
                for name, location in self.shares:
                    f.write(f'location download_{} {\n')
                    f.write(f'    root {location};\n')
                    f.write('}\n\n')

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
