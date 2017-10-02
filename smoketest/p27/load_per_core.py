from __future__ import print_function
from time import sleep
import pprint

cores = 4
#last_idle = last_total = 0
#core_info = []
nr = 0

core_info = []
core_load = {}
#core_load['core'] = {}
#core_load['core'][nr] = {}

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(core_load)

#for core_nr in range(cores):
#    core_load['core'][core_nr]['test1'] = 0 
#    core_load['core'][core_nr]['test2'] = 0 


while True:
    print("while") 
    with open('/proc/stat') as f:
        for core in range(cores):
            fields = [float(column) for column in f.readline().strip().split()[1:]]
            print(cores)
            fields = [float(column) for column in f.readline().strip().split()[1:]]
            core_info.append(fields)
    
    for core_nr in range(cores):
        print(core_info[core_nr])
        print("core" + str(core_nr))

        #core_load['core1']['idle'] = core_info[core][3]

        core_load[str(core_nr)] = {}

        core_load[str(core_nr)]['idle'] = core_info[core_nr][3]
        #core_load['core'][core_nr]['idle'] = 0
        #core_load = dict(core1_idle = core_info[core_nr][3]) 

        core_load[str(core_nr)]['total'] = sum(core_info[core_nr])
        #print("core_nr = " + str(core_nr))
        #print("core_load['core'][core_nr]['total'] = " + str(core_load['core'][core_nr]['total']))
        #idle, total = core_info[core][3], sum(core_info[core])
        #idle_delta, total_delta = idle - last_idle, total - last_total

        if 'last_idle' not in core_load[str(core_nr)]:
            print("in if statement")
            core_load[str(core_nr)]['last_idle'] = 0
            core_load[str(core_nr)]['last_total'] = 0

        core_load[str(core_nr)]['idle_delta'] = core_load[str(core_nr)]['idle'] - core_load[str(core_nr)]['last_idle'] 
        core_load[str(core_nr)]['total_delta'] = core_load[str(core_nr)]['total'] - core_load[str(core_nr)]['last_total'] 
        
        core_load[str(core_nr)]['last_idle'] = core_load[str(core_nr)]['idle']
        core_load[str(core_nr)]['last_total'] = core_load[str(core_nr)]['total']  
        #last_idle, last_total = idle, total
        #utilisation = 100.0 * (1.0 - idle_delta / total_delta)
        utilisation = 100.0 * (1.0 - core_load[str(core_nr)]['idle_delta'] / core_load[str(core_nr)]['total_delta']) 

        print("core number " + str(core_nr) + '%5.1f%%' % utilisation)
        #print("core number " + str(core) + '%5.1f%%' % utilisation, end='\r')
        sleep(1)
