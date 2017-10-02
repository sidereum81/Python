from time import sleep
import pprint
import subprocess
import shlex
import io

class CpuLoad:

    def get_data(self, cores):
        stats =  subprocess.check_output(shlex.split('cat /proc/stat'))
        #stats_data = io.StringIO(str(stats.decode("utf-8")))
        stats_data = io.StringIO(unicode(stats))
        throw_away_first_line = stats_data.readline()
        core_load = {}

        for core in range(cores):
            core_load[str(core)] = {}
            core_load[str(core)]['stats'] = [float(column) for column in stats_data.readline().strip().split()[1:]]
            core_load[str(core)]['idle'] = core_load[str(core)]['stats'][3]
            core_load[str(core)]['total'] = sum(core_load[str(core)]['stats'])

        return core_load
   

    def calc_load(self, core_first_data, core_last_data, cores):
        load = {}
        utilisation = []
        for core in range(cores):
            load[str(core)] = {}
            load[str(core)]['idle_delta'] = core_first_data[str(core)]['idle'] - core_last_data[str(core)]['idle']
            load[str(core)]['total_delta'] = core_first_data[str(core)]['total'] - core_last_data[str(core)]['total']

            utilisation.append(100.0 * (1.0 - load[str(core)]['idle_delta'] / load[str(core)]['total_delta']))

        return utilisation


if __name__ == "__main__":
    test = CpuLoad()
    while(1):
        first_data = test.get_data(4)
        sleep(1)
        second_data = test.get_data(4)
        load = test.calc_load(first_data, second_data, 4)
        for core in range(4):
            print("core" + str(core) + " has load " + str(load[core]))
        print("")
    print("******************************************")
