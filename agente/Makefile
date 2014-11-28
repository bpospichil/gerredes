CC=gcc
CFLAGS=`net-snmp-config --cflags` -fPIC -shared -g
LDLIBS=`net-snmp-config --libs`

OBJECTS=vmProcessTable.so vmUptime.so


all: $(OBJECTS)

%.so: %.c
	$(CC) $(CFLAGS) -o ../$@ $< $(LDLIBS)

clean:
	rm ../*.so
