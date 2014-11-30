from mongoengine import *
import datetime
from snimpy.manager import Manager, load
from database import ProcessTableEntry, ProcessTable, UptimeScalar, ProcessCount
import time

load("/home/bruno/.snmp/mibs/videoMgr.mib")
host = "104.131.91.218"
community = "vlavaav"
m = Manager(host, community);

def get_process_table():
    pid_list = []
    owner_list = []
    cpu_list = []
    mem_list = []
    state_list = []

    for idx in m.vmProcessOwner:
        owner_list.append(m.vmProcessOwner[idx])

    for idx in m.vmProcessPID:
        pid_list.append(m.vmProcessPID[idx])

    for idx in m.vmProcessCPU:
        cpu_list.append(m.vmProcessCPU[idx])

    for idx in m.vmProcessMem:
        mem_list.append(m.vmProcessMem[idx])

    for idx in m.vmProcessState:
        state_list.append(m.vmProcessState[idx])

    entries = []
    for elem in zip(range(1,21), pid_list, owner_list, cpu_list, mem_list, state_list):
        entry = ProcessTableEntry(index=elem[0],
                                  pid=elem[1],
                                  owner=elem[2],
                                  cpu=elem[3],
                                  mem=elem[4],
                                  state=elem[5])
        entries.append(entry)

    p = ProcessTable(entries=entries)
    p.save();

def get_uptime_scalar():
    uptime = int(m.vmUptime)
    obj = UptimeScalar(value=uptime)
    obj.save()

def update_process_count():
    count = int(m.vmProcessCount)
    last = ProcessCount.objects.order_by('-id').first()
    if last and last.value != count:
        m.vmProcessCount = last.value

if __name__ == '__main__':
    connect('gerente')
    while(True):
        get_process_table()
        get_uptime_scalar()
        update_process_count()
        time.sleep(60)

