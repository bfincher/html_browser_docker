#!/usr/bin/python3

import contextlib
import os
import pickle
import shutil
import socket
from threading import Thread
import time
import unittest

from busypie import wait, SECOND

import dynamic_update
from dynamic_update import create_instance_from_args

from mockito import mock, when

source_config_file = 'test_nginx.conf'
dest_config_file = 'testing_nginx.conf'

class DynamicUpdateTest(unittest.TestCase):
    def setUp(self):
        shutil.copyfile(source_config_file, dest_config_file)

        self.expectedData = {'share1': '/data/share1/', 'share2': '/data/share2/'}

    def tearDown(self):
        if os.path.exists(dest_config_file):
            os.remove(dest_config_file)

    def testCreateInstance(self):
        instance = create_instance_from_args()
        self.assertEqual(dynamic_update.DEFAULT_LISTEN_HOST, instance.listen_host)
        self.assertEqual(dynamic_update.DEFAULT_LISTEN_PORT, instance.listen_port)
        self.assertEqual(dynamic_update.DEFAULT_NGINX_CONFIG_FILE, instance.nginx_config_file)

        instance = create_instance_from_args(['', '--listen-host', 'testHost'])
        self.assertEqual('testHost', instance.listen_host)
        self.assertEqual(dynamic_update.DEFAULT_LISTEN_PORT, instance.listen_port)
        self.assertEqual(dynamic_update.DEFAULT_NGINX_CONFIG_FILE, instance.nginx_config_file)

        instance = create_instance_from_args(['', '--listen-port', '50'])
        self.assertEqual(dynamic_update.DEFAULT_LISTEN_HOST, instance.listen_host)
        self.assertEqual(50, instance.listen_port)
        self.assertEqual(dynamic_update.DEFAULT_NGINX_CONFIG_FILE, instance.nginx_config_file)

        instance = create_instance_from_args(['', '--nginx-config-file', 'testFile'])
        self.assertEqual(dynamic_update.DEFAULT_LISTEN_HOST, instance.listen_host)
        self.assertEqual(dynamic_update.DEFAULT_LISTEN_PORT, instance.listen_port)
        self.assertEqual('testFile', instance.nginx_config_file)

        instance = create_instance_from_args(['', '--listen-host', 'testHost',
                                              '--listen-port', '50',
                                              '--nginx-config-file', 'testFile'])
        self.assertEqual('testHost', instance.listen_host)
        self.assertEqual(50, instance.listen_port)
        self.assertEqual('testFile', instance.nginx_config_file)

    def testLoadConfig(self):
        instance = create_instance_from_args(['', '--nginx-config-file', dest_config_file])
        instance.loadConfig()
        self.assertData(instance, self.expectedData)

    def testClientConnection(self):
        instance = create_instance_from_args(['', '--nginx-config-file', dest_config_file])
        instance.loadConfig()
        t = Thread(target = instance.listen)
        t.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('localhost', dynamic_update.DEFAULT_LISTEN_PORT)
        sock.connect(address)

        try :
            self.expectedData['share3'] = 'test location 3'
            self.expectedData['share4'] = 'test location 4'

            sock.sendall(pickle.dumps(self.expectedData))
            wait().at_most(2, SECOND).until(lambda: len(instance.shares) == 4)
            self.assertData(instance, self.expectedData)

            # change one of the share locations
            self.expectedData['share1'] = '/new/location/share1'
            sock.sendall(pickle.dumps(self.expectedData))
            wait().at_most(2, SECOND).until(lambda: instance.shares['share1'] == '/new/location/share1')
            self.assertData(instance, self.expectedData)

            # remove one of the shares
            del self.expectedData['share3']
            sock.sendall(pickle.dumps(self.expectedData))
            wait().at_most(2, SECOND).until(lambda: len(instance.shares) == 3)
            self.assertData(instance, self.expectedData)
        finally:
            sock.sendall(b'quit')
            sock.close()

    def assertData(self, instance, data):
        self.assertEqual(len(data), len(instance.shares))

        for name, location in data.items():
            self.assertTrue(name in instance.shares)
            self.assertEqual(location, instance.shares[name])

        #make sure that the data in the config file is correct
        fromFile = dynamic_update.loadConfig(dest_config_file)
        print('BKF data keys = ')
        for key in data.keys():
            print(key)

        print('BKF fromFile keys = ')
        for key in fromFile.keys():
            print(key)

        self.assertEqual(data, fromFile)

if __name__ == '__main__':
    unittest.main()
