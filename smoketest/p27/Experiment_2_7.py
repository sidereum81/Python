#!/usr/bin/env python
import logging
import time
import sys
import os
from datetime import timedelta
import subprocess
import shlex
import re
import cpuload
from time import sleep

class Experiment():

    def __init__(self):
        self._logpath = "/home/kenneth/debug.txt"
        self._cpu_load = None


    def getUptime(self):
        print("getUptime")

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
        
        print(uptime_string)


    def getCpuLoad(self):
        print ("getCpuLoad")
        shell_response = self.runCommand("uptime")
        #cpu_load = self.regExp('.*load average:\s*([^\n\r]*)', 0, shell_response).split( )
        cpu_load = re.findall('.*load average:\s*([^\n\r]*)', shell_response)[0].split( )
        load_average_first_minute = cpu_load[0]
        load_average_five_minutes = cpu_load[1]
        load_average_fifteen_minutes = cpu_load[2] 

        print("Load average minute " + load_average_first_minute)
        print("Load average five minutes " + load_average_five_minutes)
        print("Load average fifteen minutes " + load_average_fifteen_minutes)


    def getCpuInfo(self):
        print("getCpuInfo")
        shell_response = self.runCommand("cat /proc/cpuinfo")
        model_name = re.findall('model\s*name\s*:\s*([^\n\r]*)', shell_response)[0]
        #model_name = self.regExp('model\s*name\s*:\s*([^\n\r]*)', 0, shell_response)
        #number_of_cores = self.regExp('cpu\s*cores\s*:\s*(\d+)', 0, shell_response)
        number_of_cores = re.findall('cpu\s*cores\s*:\s*(\d+)', shell_response)[0]

        load = cpuload.CpuLoad()
        first_cpu_data = load.get_data(int(number_of_cores))
        sleep(1)
        second_cpu_data = load.get_data(int(number_of_cores))
        total_load = load.calc_load(first_cpu_data, second_cpu_data, int(number_of_cores))

        for core in range(int(number_of_cores)):
            print("load in core" + str(core) + " = " + '%5.1f%%' % total_load[core])
        print("Cpu cores: " + number_of_cores)
        print("model_name: " + model_name)


    def getMemStatus(self):
        print ("getMemStatus")
        shell_response = self.runCommand("free -m")
        #memory_list = self.regExp('.*Mem:\s*([^\n\r]*)', 0, shell_response).split( )
        memory_list = re.findall('.*Mem:\s*([^\n\r]*)', shell_response)[0].split( )
        total_memory = float(memory_list[0])
        used_memory = float(memory_list[1])
        
        free = 100 * (1 - (used_memory/total_memory))

        print("total_memory: " + str(total_memory))
        print("used_memory: "+ str(used_memory))
        print("free " + str(free))
        print("free = {:.2f}".format(free) + "%")

        print("The total memory is: " + str(total_memory))
        print("The used memory is: " + str(used_memory))

    def runCommand(self, command):
        shell_response = subprocess.check_output(shlex.split(command)).decode('utf-8')
        return shell_response
   

#    def regExp(self, reg_expression, position, text):
#        regular = re.compile(reg_expression)
#        restult_text = re.findall(regular, text)[position]
#        return restult_text

if __name__ == "__main__":
    Experiment().getUptime()
    Experiment().getCpuLoad()
    Experiment().getMemStatus()
    Experiment().getCpuInfo()
