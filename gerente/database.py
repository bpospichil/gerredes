from mongoengine import *
import datetime
from snimpy.manager import Manager, load

load("/home/bruno/.snmp/mibs/videoMgt.mib")
host = "104.131.91.218"
community = "vlavaav"
m = Manager(host, community);


class ProcessTableEntry(EmbeddedDocument):
    index = IntField(required=True)
    pid = IntField(required=True)
    owner = StringField(required=False)
    cpu = IntField()
    mem = IntField()
    state = StringField(max_length=5, required=False)

class ProcessTable(Document):
    entries = ListField(EmbeddedDocumentField(ProcessTableEntry))
    timestamp = DateTimeField(default = datetime.datetime.now)
   
class UpTimeScalar(Document):
    value = DateTimeField()
    timestamp = DateTimeField()

 

connect('gerente')

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
p.save()

