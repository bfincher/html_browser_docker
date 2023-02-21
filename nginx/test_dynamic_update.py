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

class WaitForeverTask:
    def __init__(self):
        self.keepRunning = True

    def waitForever(self):
        while self.keepRunning:
            time.sleep(1)

@contextlib.contextmanager
def socket_socket_func(scket):
    yield scket

class DynamicUpdateTest(unittest.TestCase):
    def mockedListen(self):
        result = next(listenResult)
        if result == -1:
            t = WaitForeverTask()
            self.threads.append(t)

            thread = Thread(target=t.waitForever)
            thread.start()
            thread.join()

    def setUp(self):
        shutil.copyfile(source_config_file, dest_config_file)
        self.threads = []

    def createMocks(self):
        listenResult = [None, -1]
        self.listenIter = iter(listenResult)


        self.instance = create_instance_from_args(['', '--listen-host', 'testHost',
                                                   '--listen-port', '50',
                                                   '--nginx-config-file', 'testFile'])

        conn = mock()
        data = [{'shareName': 'share3', 'location': 'test location 3'},
                {'shareName': 'share4', 'location': 'test location 4'}]
        when(conn).recv(...).thenReturn(data)

        scket = mock()
        when(scket).listen().thenReturn(self.mockedListen)


        when(scket).accept().thenReturn(('testIp', conn))
        when(scket).close().thenReturn(None)
#        when(scket).__enter__().thenReturn(scket)
#        when(scket).__exit__(...)
        when(scket).setblocking = False
        when(scket).fileno = 1

        when(socket).socket(...).thenReturn(lambda: socket_socket_func(scket))

    def tearDown(self):
        if os.path.exists(dest_config_file):
            os.remove(dest_config_file)

        for thread in self.threads:
            thread.keepRunning = False

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

    def test(self):
        self.createMocks()

        s = socket.socket('bla', 'bla')
        print(type(s))

        instance = create_instance_from_args(['', '--nginx-config-file', dest_config_file])
        instance.loadConfig()
        t = Thread(target = instance.listen)
        t.start()

        #wait().at_most(100, SECOND).until(lambda: len(self.threads) > 0)

def test():
    data = [{'shareName': 'share3', 'location': 'test location 3'},
            {'shareName': 'share4', 'location': 'test location 4'}]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 5000))
        s.sendall(pickle.dumps(data))

if __name__ == '__main__':
    unittest.main()
