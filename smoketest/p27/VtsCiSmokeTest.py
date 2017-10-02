#!/usr/bin/env python

import logging
import time
import sys
import os
import re
import cpuload
from time import sleep

from vts.runners.host import asserts
from vts.runners.host import base_test
from vts.runners.host import const
from vts.runners.host import test_runner
from vts.utils.python.controllers import android_device

class VtsCiSmokeTest(base_test.BaseTestClass):
    """Two hello world test cases which use the shell driver."""


    def setUpClass(self):
        self.dut = self.registerController(android_device)[0]


    def testEcho1(self):
        """A simple testcase which sends a command."""
        self.dut.shell.InvokeTerminal("first_shell")  # create a remote shell instance.
        self.dut.shell.first_shell.Execute("setenforce 0")  # SELinux permissive mode
        kernel_version = self.dut.shell.shell_one.Execute("uname -r")  # runs a shell command.
        logging.info(kernel_version)


    def testEcho2(self):
        """A simple testcase which sends two commands."""
        self.dut.shell.InvokeTerminal("my_shell2")
        my_shell = getattr(self.dut.shell, "my_shell2")
        results = my_shell.Execute(["echo hello", "echo world"])
        logging.info(str(results[const.STDOUT]))
        asserts.assertEqual(len(results[const.STDOUT]), 2)  # check the number of processed commands
        asserts.assertEqual(results[const.STDOUT][0].strip(), "hello")
        asserts.assertEqual(results[const.STDOUT][1].strip(), "world")
        asserts.assertEqual(results[const.EXIT_CODE][0], 0)
        asserts.assertEqual(results[const.EXIT_CODE][1], 0)

    def testCpuLoad(self):
        shell_response = self.runCommand("cat /proc/cpuinfo")
        model_name = self.regExp('.*model name	:\s*([^\n\r]*)', 0, shell_response)
        number_of_cores = self.regExp('.*cpu cores	:\s*([^\n\r]*)', 0, shell_response)

        load = cpuload.CpuLoad()
        first_cpu_data = load.get_data(int(number_of_cores))
        sleep(1)
        second_cpu_data = load.get_data(int(number_of_cores))
        total_load = load.calc_load(first_cpu_data, second_cpu_data, int(number_of_cores))

        for core in range(int(number_of_cores)):
            print("load in core" + str(core) + " = " + str('%.1f%%' % total_load[core]))
            asserts.assertLess(total_load[core], 90)
        print("Cpu cores: " + number_of_cores)
        print("model_name: " + model_name)
        
    def testMemory(self):
        shell_response = self.runCommand("free -h")
        memory_list = self.regExp('.*Mem:\s*([^\n\r]*)', 0, shell_response).split( )
        total_memory = memory_list[0]
        used_memory = memory_list[1]
        
        calc_total_m = float(re.findall('[\d,.]+', total_memory)[0].replace(',', '.'))
        calc_used_m = float(re.findall('[\d,.]+', used_memory)[0].replace(',', '.'))
        free = 100 * (1 - calc_used_m/calc_total_m)

        asserts.assertLess(10, free)

        print("The used memory is: " + used_memory)
        print("The total memory is: " + total_memory)
        print("Free memory is: {:.2f}".format(free))

if __name__ == "__main__":
    test_runner.main()
