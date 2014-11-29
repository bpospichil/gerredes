gerredes
========

Estrutura da MIB
--------
```
+--videoMgr(1)
   |
   +-- -R-- TimeTicks vmUptime(1)
   +-- -RW- INTEGER   vmProcessCount(2)
   |        Range: 0..255
   |
   +--vmProcessTable(3)
   |  |
   |  +--vmProcessEntry(1)
   |     |  Index: vmProcessIndex
   |     |
   |     +-- -R-- INTEGER   vmProcessIndex(1)
   |     +-- -R-- INTEGER   vmProcessPID(2)
   |     +-- -R-- String    vmProcessOwner(3)
   |     +-- -R-- INTEGER   vmProcessCPU(4)
   |     |        Range: 0..100
   |     +-- -R-- INTEGER   vmProcessMem(5)
   |     |        Range: 0..100
   |     +-- -R-- String    vmProcessState(6)
   |
   +--vmChannelTable(4)
   |  |
   |  +--vmChannelEntry(1)
   |     |  Index: vmChannelId
   |     |
   |     +-- -R-- INTEGER   vmChannelId(1)
   |     +-- -R-- INTEGER   vmChannelAudience(2)
   |
   +--vmVideoTable(5)
      |
      +--vmVideoEntry(1)
         |  Index: vmVideoId
         |
         +-- -R-- INTEGER   vmVideoId(1)
         +-- -R-- INTEGER   vmVideoAudience(2)
         +-- -RW- INTEGER   vmVideoAdvertisingMetrics(3)
         +-- -R-- INTEGER   vmVideoKindVOD(4)
         |        Range: 0..1
         +-- -R-- INTEGER   vmVideoKindLive(5)
                  Range: 0..1
```
