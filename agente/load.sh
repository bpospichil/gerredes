#!/bin/bash

set -e

ID='-v2c -c vlavaav localhost'

snmpset $ID UCD-DLMOD-MIB::dlmodStatus.1 i create
snmpset $ID UCD-DLMOD-MIB::dlmodName.1 s "vmUptime" UCD-DLMOD-MIB::dlmodPath.1 s "/home/bruno/gerredes/vmUptime.so"
snmpset $ID UCD-DLMOD-MIB::dlmodStatus.1 i load

snmpset $ID UCD-DLMOD-MIB::dlmodStatus.2 i create
snmpset $ID UCD-DLMOD-MIB::dlmodName.2 s "vmProcessTable" UCD-DLMOD-MIB::dlmodPath.2 s "/home/bruno/gerredes/vmProcessTable.so"
snmpset $ID UCD-DLMOD-MIB::dlmodStatus.2 i load

snmpset $ID UCD-DLMOD-MIB::dlmodStatus.3 i create
snmpset $ID UCD-DLMOD-MIB::dlmodName.3 s "vmProcessCount" UCD-DLMOD-MIB::dlmodPath.3 s "/home/bruno/gerredes/vmProcessCount.so"
snmpset $ID UCD-DLMOD-MIB::dlmodStatus.3 i load

#snmpset $ID UCD-DLMOD-MIB::dlmodStatus.3 i create
#snmpset $ID UCD-DLMOD-MIB::dlmodName.3 s "vmVideoTable" UCD-DLMOD-MIB::dlmodPath.3 s "/home/bruno/gerredes/vmVideoTable.so"
#snmpset $ID UCD-DLMOD-MIB::dlmodStatus.3 i load
