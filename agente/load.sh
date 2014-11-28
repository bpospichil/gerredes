#!/bin/bash

set -e

ID='-v2c -c vlavaav localhost'

snmpset $ID UCD-DLMOD-MIB::dlmodStatus.1 i create

snmpset $ID UCD-DLMOD-MIB::dlmodName.1 s "vmUptime" UCD-DLMOD-MIB::dlmodPath.1 s "/home/bruno/gerredes/vmUptime.so"

snmpset $ID UCD-DLMOD-MIB::dlmodStatus.1 i load
