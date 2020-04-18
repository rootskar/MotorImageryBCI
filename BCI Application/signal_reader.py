#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import uuid

from server_process import ServerProcess
from utils import divide_chunks


class SignalReader(object):

    def __init__(self, tcp_ip='127.0.0.1', tcp_port=5151, device_type=2, buffer_size=1024, mock_server=False):
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        sec_key = uuid.uuid4().hex.upper()[0:20]
        self.WEBSOCKET_KEY = str.encode('Sec-WebSocket-Key: ' + sec_key)
        self.socket = None
        self.server_process = ServerProcess(tcp_ip, tcp_port, device_type, mock=mock_server)

    def open_stream(self):
        self.server_process.start()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.tcp_ip, self.tcp_port))
        self.socket.sendall(self.WEBSOCKET_KEY)

    def close_stream(self):
        if self.socket:
            self.socket.close()
        self.server_process.stop()

    def read_signals(self, max_size):
        data_array = []
        while len(data_array) < max_size:  # 14 x 640 = 8960
            second_array = []
            while len(second_array) < 1792:
                data = self.socket.recv(self.buffer_size).decode('utf-8').split("\r\n")
                for data_chunk in data:
                    converted_data = []
                    for elem in data_chunk.split(","):
                        try:
                            converted_data.append(int(elem))
                        except:
                            pass
                    second_array.extend(converted_data)
                time.sleep(0.5)
                data_array.extend(second_array)

        return list(divide_chunks(data_array[:max_size], 14))
