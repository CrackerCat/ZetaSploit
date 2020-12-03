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
from core.options import options

class module:
    def __init__(self):
        self.badges = badges()
        self.options = options()
        
    def show_details(self, details):
        print(self.badges.I + "Module Name: " + details['Name'])
        authors = ""
        for author in details['Authors']:
            authors += author + " "
        print(self.badges.I + "Module Authors: " + authors.strip())
        print(self.badges.I + "Module Description: " + details['Description'])
        print(self.badges.I + "Module Comment: " + details['Comment'])
        
    def console(self, modules, module):
        current_module = []
        pwd = 0
        current_module.append('')
        current_module[pwd] = module
        while True:
            try:
                command = input('\033[4mzsf\033[0m(\033[1;31m'+current_module[pwd].details['Name']+'\033[0m)> ').strip()
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
                    print("    details        Show specified modules details.")
                    print("    exec           Execute system command.")
                    print("    exit           Exit ZetaSploit Framework.")
                    print("    help           Show available commands.")
                    print("    modules        Show available modules.")
                    print("")
                    print("Module Commands")
                    print("===============")
                    print("")
                    print("    options        Show current modules options.")
                    print("    run            Run current modules.")
                    print("    set            Set an option value.")
                    print("    use            Select specified modules.")
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
                        print("Usage: use <modules>")
                    else:
                        if command[1] in modules.keys():
                            current_module.append('')
                            pwd += 1
                            current_module[pwd] = commands[1]
                        else:
                            print(self.badges.E + "Unrecognized modules!")
                elif commands[0] == "modules":
                    for name in modules.keys():
                        if current_module[pwd].details['Name'] == name:
                            print('\033[1;31m'+name+'\033[0m')
                        else:
                            print(name)
                elif commands[0] == "back":
                    pwd -= 1
                    current_module = current_module[0:-1]
                    if current_module == []:
                        pwd = 0
                        break
                elif commands[0] == "options":
                    self.options.parse_options(current_module[pwd].options)
                elif commands[0] == "set":
                    if len(commands) < 3:
                        print("Usage: set <option> <value>")
                    else:
                        if commands[1] in current_module[pwd].options.keys():
                            print(self.badges.I + commands[1] + " ==> " + commands[2])
                            current_module[pwd].options[commands[1]]['Value'] = commands[2]
                        else:
                            print(self.badges.E + "Unrecognized option!")
                elif commands[0] == "run":
                    count = 0
                    for option in current_module[pwd].options.keys():
                        if current_module[pwd].options[option]['Value'] == '' and current_module[pwd].options[option]['Required'] == True:
                            count += 1
                    if count > 0:
                        print(self.badges.E + "Missed some required options! ("+count+")")
                    else:
                        current_module[pwd].run()
                else:
                    print(self.badges.E + "Unrecognized command!")
            except (KeyboardInterrupt, EOFError):
                print("")
            except Exception as e:
                print(self.badges.E +"An error occurred: "+str(e)+"!")