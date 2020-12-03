#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from core.badges import badges
from core.helper import helper

from data.linux.reverse_tcp.zeterpreter.core.transfer import transfer
from data.linux.reverse_tcp.zeterpreter.core.handler import handler

class controller:
    def __init__(self, client):
        self.client = client
        self.badges = badges()
        self.helper = helper()

        self.transfer = transfer(client)
        self.handler = handler(client)

    def close_connection(self):
        self.send_command("exit", None, False)
        self.client.close()

    def send_command(self, command, args=None, ask_for_status=True):
        buffer = command
        if args != None:
            buffer += " " + args

        terminator = self.handler.sendall(buffer)
        result = self.handler.recvall(terminator)

        if ask_for_status:
            if result == "error":
                return ("error", "")
            else:
                return ("success", result.decode().strip())

    def download(self, input_file, output_path):
        self.transfer.download(input_file, output_path)

    def upload(self, input_file, output_path):
        self.transfer.upload(input_file, output_path)
