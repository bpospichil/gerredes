gerredes
========

Estrutura da MIB
--------
```
snmptranslate -Tp -IR videoMgr
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
   |     |  Index: vmChannelIndex
   |     |
   |     +-- -R-- INTEGER   vmChannelIndex(1)
   |     +-- -R-- INTEGER   vmChannelId(2)
   |     +-- -R-- INTEGER   vmChannelAudience(3)
   |
   +--vmVideoTable(5)
      |
      +--vmVideoEntry(1)
         |  Index: vmVideoIndex
         |
         +-- -R-- INTEGER   vmVideoIndex(1)
         +-- -R-- INTEGER   vmVideoId(2)
         +-- -R-- INTEGER   vmVideoAudience(3)
         +-- -RW- INTEGER   vmVideoAdvertisingMetrics(4)
         +-- -R-- INTEGER   vmVideoKindVOD(5)
         |        Range: 0..1
         +-- -R-- INTEGER   vmVideoKindLive(6)
                  Range: 0..1

```
