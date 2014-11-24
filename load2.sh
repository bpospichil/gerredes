#!/bin/bash

set -e

ID='-v2c -c vlavaav localhost'

snmpset $ID UCD-DLMOD-MIB::dlmodStatus.2 i create

snmpset $ID UCD-DLMOD-MIB::dlmodName.2 s "vmProcessTable" UCD-DLMOD-MIB::dlmodPath.2 s "/home/bruno/gerredes/vmProcessTable.so"

snmpset $ID UCD-DLMOD-MIB::dlmodStatus.2 i load
