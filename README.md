Gerência de Redes
========

Estrutura da MIB
--------
```
$ snmptranslate -Tp -IR videoMgr
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

Gerando os agentes
--------
Os agentes foram gerados utilizando o utilitário mib2c e compilados de acordo com make usando o arquivo agente/Makefile.
Para dados escalares foi utilizado:
```
$ mib2c -c mib2c.scalar.conf <ID>

```
E para dados tabulares:
```
 mib2c -c mib2c.create-dataset.conf <ID>
```
Essas configurações são bastante simples, porém atendem as expectativas desse trabalho. Em casos mais reais, existem outras configurações possíveis, como pode ser visto em http://www.net-snmp.org/docs/man/mib2c.html

Carregando os agentes
--------
Os agentes foram carregados por meio de sets efetuados na MIB UCD-DLMOD-MIB. Os comandos utilizados para uma mib qualquer são:
```
snmpset -v2c -c <COMMUNITY> <HOST> UCD-DLMOD-MIB::dlmodStatus.<N> i create
snmpset -v2c -c <COMMUNITY> <HOST> UCD-DLMOD-MIB::dlmodName.<N> s <MIBNAME> UCD-DLMOD-MIB::dlmodPath.<N> s <MIBPATH>
snmpset -v2c -c <COMMUNITY> <HOST> UCD-DLMOD-MIB::dlmodStatus.<N> i load
```
Aonde:
* COMMUNITY é a comunidade;
* HOST é o endereço do servidor;
* N é um numero inteiro indice da tabela. Não pode ser repetido;
* MIBNAME é o nome da entrada na MIB (e.g. sysUptime);
* MIBPATH é o caminho até a so (shared object) que responde por essa mib;

Carregando o gerente
--------
O gerente foi desenvolvido em Python e utiliza mongodb como espaço de troca.
As bibliotecas instaladas no ambiente são:
```
Flask==0.10.1
Flask-WTF==0.10.3
Jinja2==2.7.3
Logbook==0.8.0
MarkupSafe==0.23
Pygments==2.0.1
Quandl==2.0
Sphinx==1.2.3
WTForms==2.0.1
Werkzeug==0.9.6
cffi==0.8.6
flask-mongoengine==0.7.1
ipython==2.3.1
itsdangerous==0.24
matplotlib==1.4.2
mock==1.0.1
mongoengine==0.8.7
nose==1.3.4
numpy==1.9.1
numpydoc==0.5
patsy==0.3.0
pyasn1==0.1.7
pycparser==2.10
pycrypto==2.6.1
pymongo==2.7.2
pyparsing==2.0.3
pysnmp==4.2.5
python-dateutil==2.2
pytz==2014.10
requests==2.4.3
six==1.8.0
snimpy==0.8.3
statsmodels==0.6.0
sympy==0.7.6
tornado==4.0.2
zipline==0.7.0
```

Além disso o gerente foi dividido em dois executáveis:
* manager.py: responsável por consultar o mongodb e gerar a interface
* daemon.py: responsável por coletar informações usando snmp e gravar no mongodb.
