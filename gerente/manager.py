from flask import Flask, render_template, abort
from database import ProcessTable, ProcessTableEntry
from mongoengine import connect

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO

app = Flask(__name__)

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

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(mem_list[::-1])
    plt.xlabel('Data/Hora (EST)', labelpad=20)
    plt.ylabel('Uso de memoria (MB)')
    plt.tight_layout()
    ax.legend()
    plt.margins(0.05)
    plt.xticks(range(0, len(timestamp_list)))
    plt.subplots_adjust(bottom=0.3, right=0.95)
    ax.set_xticklabels(timestamp_list[::-1], rotation=45)
    io = StringIO()
    fig.savefig(io, format='png')
    graph = io.getvalue().encode('base64')
    
    return render_template("process_table_detail.html",
                           title='vmProcessMem.{0}'.format(id),
                           data=zip(timestamp_list, mem_list),
                           graph=graph,
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

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ind = np.arange(len(cpu_list))
    ax.bar(ind, cpu_list[::-1])
    plt.xticks(ind + .3 / 2, timestamp_list[::-1])
    plt.xlabel('Data/Hora (EST)', labelpad=20)
    plt.ylabel('Uso de CPU (%)')
    plt.margins(xmargin=0.05)
    plt.xticks(range(0, len(timestamp_list)))
    plt.subplots_adjust(bottom=0.3, right=0.95)
    ax.set_xticklabels(timestamp_list[::-1], rotation=45)

    io = StringIO()
    fig.savefig(io, format='png')
    graph = io.getvalue().encode('base64')

    return render_template("process_table_detail.html",
                           title='vmProcessCPU.{0}'.format(id),
                           data=zip(timestamp_list, cpu_list),
                           graph=graph,
                           ref_table='CPU (%)')

if __name__ == "__main__":
    connect("gerente")
    app.run('0.0.0.0', debug=True)
