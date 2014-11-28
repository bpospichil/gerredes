from flask import Flask, render_template, abort
from database import ProcessTable, ProcessTableEntry, UptimeScalar
from mongoengine import connect

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO

import time

app = Flask(__name__)

def gen_graph(kind, xvals, yvals, xlabel, ylabel):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ind = np.arange(len(yvals))

    if kind == 'line':
        ax.plot(ind, yvals[::-1])
    elif kind == 'bar':
    	ax.bar(ind, yvals[::-1])

    plt.xticks(ind + .3 / 2, xvals[::-1])
    plt.xlabel(xlabel, labelpad=20)
    plt.ylabel(ylabel)
    plt.margins(xmargin=0.05)
    plt.xticks(range(0, len(xvals)))
    plt.subplots_adjust(bottom=0.3, right=0.9)
    ax.set_xticklabels(xvals[::-1], rotation=45)
    io = StringIO()
    fig.savefig(io, format='png')
    graph = io.getvalue().encode('base64')
    return graph

@app.route("/vmUptime/")
def uptime():
    objs = UptimeScalar.objects.all()
    last = objs.order_by('-id').first()
    maxuptime = 0
    for obj in objs:
        if int(obj.value) > maxuptime:
            maxuptime = int(obj.value)
    return render_template('scalar.html',
                           title='vmUptime',
                           date=last.timestamp.strftime("%x - %X"),
                           uptime=time.strftime('%X', time.gmtime(int(last.value))),
                           maxuptime=time.strftime('%X', time.gmtime(maxuptime)),
                           kind='Uptime')


@app.route("/vmProcessTable/")
def process_table():
    p = ProcessTable.objects.order_by('-id').first()
    return render_template("process_table.html", 
		           title='vmProcessTable',
                           entries=p.entries, 
                           date=p.timestamp.strftime("%x - %X"))

@app.route("/vmProcessMem/<int:id>")
def process_table_mem(id):

    if id <= 0 or id >=20:
        return abort(404);

    mem_list = []
    timestamp_list = []
    for p in ProcessTable.objects.order_by('-id'):
        mem_list.append(p.entries[id-1].mem)
        timestamp_list.append(p.timestamp.strftime("%x - %X"))
   
    return render_template("process_table_detail.html",
                           title='vmProcessMem.{0}'.format(id),
                           data=zip(timestamp_list, mem_list),
                           graph=gen_graph('line',
                                           timestamp_list,
                                           mem_list,
                                           'Data/Hora (EST)',
                                           'Uso de memoria (MB)'),
                           ref_table='Memoria (MB)')

@app.route("/vmProcessCPU/<int:id>")
def process_table_cpu(id):

    if id < 0 or id > 20:
        return abort(404)

    cpu_list = []
    timestamp_list = []
    for p in ProcessTable.objects.order_by('-id'):
        cpu_list.append(float(p.entries[id-1].cpu)/20)
        timestamp_list.append(p.timestamp.strftime("%x - %X"))

    return render_template("process_table_detail.html",
                           title='vmProcessCPU.{0}'.format(id),
                           data=zip(timestamp_list, cpu_list),
                           graph=gen_graph('bar',
                                           timestamp_list,
                                           cpu_list,
                                           'Data/Hora (EST)',
                                           'Uso de CPU (%)'),
                           ref_table='CPU (%)')

if __name__ == "__main__":
    connect("gerente")
    app.run('0.0.0.0', debug=True)
