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

import sys
import time
import threading
import os

from core.badges import badges
from core.helper import helper

class loader:
    def __init__(self):
        self.badges = badges()
        self.helper = helper()

    def get_module(self, mu, name, folderpath):
        folderpath_list = folderpath.split(".")
        for i in dir(mu):
            if i == name:
                pass
                return getattr(mu, name)
            else:
                if i in folderpath_list:
                    i = getattr(mu, i)
                    return self.get_module(i, name, folderpath)

    def import_plugins(self, plugin_owner, plugin_system, controller):
        plugins = dict()
        plugin_path = "plugins/" + plugin_owner + "/" + plugin_system
        for plugin_type in os.listdir(plugin_path):
            plugin_path = plugin_path + "/" + plugin_type
            for plugin in os.listdir(plugin_path):
                if plugin == '__init__.py' or plugin[-3:] != '.py':
                    continue
                else:
                    try:
                        plugin_directory = plugin_path.replace("/", ".").replace("\\", ".") + "." + plugin[:-3]
                        plugin_file = __import__(plugin_directory)
                        plugin_object = self.get_module(plugin_file, plugin[:-3], plugin_directory)
                        plugin_object = plugin_object.ZetaSploitPlugin(controller)
                        plugins[plugin_object.details['Name']] = plugin_object
                    except Exception as e:
                        print(self.badges.E + "Failed to load plugin! Reason: "+str(e))
        return plugins
    
    def import_modules(self):
        modules = dict()
        module_path = "modules"
        for module_system in os.listdir(module_path):
            module_path = module_path + "/" + module_system
            for module_type in os.listdir(module_path):
                module_path = module_path + "/" + module_type
                for module in os.listdir(module_path):
                    if module == '__init__.py' or module[-3:] != '.py':
                        continue
                    else:
                        try:
                            module_directory = module_path.replace("/", ".").replace("\\", ".") + "." + module[:-3]
                            module_file = __import__(module_directory)
                            module_object = self.get_module(module_file, module[:-3], module_directory)
                            module_object = module_object.ZetaSploitModule()
                            modules[module_object.details['Name']] = module_object
                        except Exception as e:
                            print(self.badges.E + "Failed to load plugin! Reason: " + str(e))
        return modules

    def load_plugins(self, owner, system, controller):
        plugins = self.import_plugins(owner, system, controller)
        return plugins

    def load_modules(self):
        modules = self.import_modules()
        return modules