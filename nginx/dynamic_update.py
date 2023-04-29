#!/usr/bin/python3

import pickle
import re
import socket
import sys

DEFAULT_LISTEN_HOST = '0.0.0.0'
DEFAULT_LISTEN_PORT = 5000
DEFAULT_NGINX_CONFIG_FILE = '/etc/nginx/conf.d/default.conf'

SHARE_NAME_REGEX = re.compile(r'location /download_([ a-zA-Z_0-9-]+)/\s+{')
SHARE_LOCATION_REGEX = re.compile(r'alias (.*);')

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
            locationFound = False
            while not locationFound:
                line = lines[i].strip()
                match = SHARE_LOCATION_REGEX.match(line)
                if match:
                    shares[share_name] = match.group(1)
                    locationFound = True
                i += 1

    return shares

class DynamicUpdate:
    def __init__(self, listen_host, listen_port, nginx_config_file):
        self.shares = {}
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.nginx_config_file= nginx_config_file

    def loadConfig(self):
        self.shares = loadConfig(self.nginx_config_file)

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.listen_host, self.listen_port)
        s.bind(address)
        shouldContinue = True

        while shouldContinue:
            s.listen()
            conn, addr = s.accept()
            print(f'Connected to {addr}')

            with conn:
                while True:
                    data = conn.recv(1024)
                    if data == b'quit':
                        print('Received quit command')
                        shouldContinue = False
                        break
 
                    if not data:
                        break
                    self.handle_new_share(data)

        s.close()

    def handle_new_share(self, dataStr):
        data_changed = False
        data = pickle.loads(dataStr)

        keysToDelete = [key for key in self.shares if key not in data]
        if keysToDelete:
            data_changed = True
            for key in keysToDelete:
                del self.shares[key]

        for name, location in data.items():
            if name in self.shares:
                if location != self.shares[name]:
                    self.shares[name] = location
                    data_changed = True
            else:
                self.shares[name] = location
                data_changed = True

        if data_changed:
            with open(self.nginx_config_file, 'r') as f:
                lines = f.readlines()

            with open(self.nginx_config_file, 'w') as out:
                skipLine = False
                for line in lines:
                    if not skipLine:
                        out.write(line)

                    if line.startswith('#BEGIN_DYNAMIC_CONFIG'):
                        skipLine = True
                        for name, location in self.shares.items():
                            if not name.endswith('/'):
                                name = name + '/'
                            if not location.endswith('/'):
                                location = location + '/'
                            out.write(f'    location /download_{name} {{\n')
                            out.write('        #Only allow internal redirects\n')
                            out.write('        internal;\n')
                            out.write(f'        alias {location};\n')
                            out.write('    }\n\n')
                    elif line.startswith('#END_DYNAMIC_CONFIG'):
                        skipLine = False


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
