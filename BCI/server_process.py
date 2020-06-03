#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Karel Roots"

import atexit
import socket
import subprocess
import sys
from random import randint

from PyQt5 import QtCore
from worker import Worker


class ServerProcess(object):

    def __init__(self, tcp_ip, tcp_port, device_type, mock=False):
        self.PYTHON_PATH = sys.executable
        self.CYKIT_PATH = '.\lib\CyKit\CyKIT.py'
        self.RUN_PARAMS = 'float+nocounter+generic+noheader+nobattery+ovsamples:1792'
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.device_type = device_type
        self.mock = mock
        self.mock_running = False
        self.threadpool = QtCore.QThreadPool()

    def run(self, tcp_ip, tcp_port, device_type, run_args, progress_callback):
        with open('server_logs.txt', 'a') as f:
            self.server_process = subprocess.Popen(
                [self.PYTHON_PATH, self.CYKIT_PATH, tcp_ip, str(tcp_port), str(device_type), run_args],
                stdout=f,
                stderr=f,
                shell=False)

            # kill server process on program exit
            atexit.register(self.server_process.kill)

    def mock_run(self, tcp_ip, tcp_port, progress_callback):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((tcp_ip, tcp_port))
        sock.listen(1)
        try:
            self.mock_con, address = sock.accept()
            self.mock_running = True
            print("Connected {}".format(address))
            while self.mock_running:
                random_data = str.encode(self.get_random_data())
                self.mock_con.sendall(random_data)
        except socket.error:
            print("Socket closed")

    def start(self):
        if self.mock:
            self.mock_start()
        else:
            worker = Worker(self.run, self.tcp_ip, self.tcp_port, self.device_type, self.RUN_PARAMS)
            self.threadpool.start(worker)

    def stop(self):
        if self.mock:
            self.mock_stop()
        else:
            self.thread_running = False

    def mock_start(self):
        worker = Worker(self.mock_run, self.tcp_ip, self.tcp_port)
        self.threadpool.start(worker)

    def mock_stop(self):
        self.mock_running = False

    def get_random_data(self):
        return ', '.join(str(randint(0, 9)) for i in range(8096))
