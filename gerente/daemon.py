from mongoengine import *
import datetime
from snimpy.manager import Manager, load
from database import ProcessTableEntry, ProcessTable, UptimeScalar, ProcessCount, VideoTableEntry, VideoTable
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

def get_video_table():
    ident_list = []
    audience_list = []
    advertising_list = []
    vod_list = []
    live_list = []

    for idx in m.vmVideoId:
        ident_list.append(m.vmVideoId[idx])

    for idx in m.vmVideoAudience:
        audience_list.append(m.vmVideoAudience[idx])

    for idx in m.vmVideoAdvertisingMetrics:
        advertising_list.append(m.vmVideoAdvertisingMetrics[idx])

    for idx in m.vmVideoKindVOD:
        vod_list.append(m.vmVideoKindVOD[idx])

    for idx in m.vmVideoKindLive:
        live_list.append(m.vmVideoKindLive[idx])

    entries = []
    for elem in zip(range(1,31), ident_list, audience_list, advertising_list, vod_list, live_list):
        entry = VideoTableEntry(index=elem[0],
                                  ident=elem[1],
                                  audience=elem[2],
                                  advertising=elem[3],
                                  vod=elem[4],
                                  live=elem[5])
        entries.append(entry)
    v = VideoTable(entries=entries)
    v.save()

if __name__ == '__main__':
    connect('gerente')
    int i = 0;
    while(True):
        update_process_count()
	if i == 20:
            i = 0
        if i == 0:
            get_process_table()
            get_uptime_scalar()
            get_video_table()
        i++
        time.sleep(30)

