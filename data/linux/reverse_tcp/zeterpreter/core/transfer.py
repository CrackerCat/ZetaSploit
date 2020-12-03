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

import os
import time

from core.helper import helper
from core.badges import badges
from core.fsmanip import fsmanip

from data.linux.reverse_tcp.zeterpreter.core.handler import handler

class transfer:
    def __init__(self, client):
        self.client = client
        self.helper = helper()
        self.badges = badges()
        self.fsmanip = fsmanip()
        self.handler = handler(client)

    def download(self, input_file, output_path):
        exists, path_type = self.fsmanip.exists_directory(output_path)
        if exists:
            if path_type != "file":
                if output_path[-1] == "/":
                    output_path = output_path + os.path.split(input_file)[1]
                else:
                    output_path = output_path + "/" + os.path.split(input_file)[1]
            terminator = self.handler.sendall("download " + input_file)
            status = self.handler.recvstr().decode().strip()
            if status == "success":
                print(self.badges.G + "Downloading " + input_file + "...")
                self.handler.recvfile(terminator, output_path)
                print(self.badges.G + "Saving to " + output_path + "...")
                print(self.badges.S + "Saved to " + output_path + "!")
            else:
                _ = self.handler.recvall(terminator).decode().strip()
                print(self.badges.E + status)

    def upload(self, input_file, output_path):
        if self.fsmanip.file(input_file):
            output_directory = output_path
            output_filename = os.path.split(input_file)[1]
            terminator = self.handler.sendall("upload " + output_directory + ":" + output_filename)
            status = self.handler.recvstr().decode().strip()
            if status == "success":
                print(self.badges.G + "Uploading " + input_file + "...")
                with open(input_file, "rb") as wf:
                    for data in iter(lambda: wf.read(4100), b""):
                        try:
                            self.handler.send(data)
                        except (KeyboardInterrupt, EOFError):
                            wf.close()
                            self.handler.send("error")
                            print(self.badges.E + "Failed to upload!")
                            return
                self.handler.send(terminator)
                print(self.badges.G + self.handler.recvstr().decode().strip())
                print(self.badges.S + self.handler.recvstr().decode().strip())
                _ = self.handler.recvall(terminator)
            else:
                _ = self.handler.recvall(terminator)
                print(self.badges.E + status)
