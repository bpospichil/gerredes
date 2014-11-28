from flask import Flask, render_template
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
    return render_template("process_table.html", title='vmProcessTable', entries=p.entries)

@app.route("/vmProcessMem/<int:id>")
def process_table_detail(id):
    mem_list = []
    timestamp_list = []
    for p in ProcessTable.objects.order_by('-id'):
        mem_list.append(p.entries[id].mem)
        timestamp_list.append(p.timestamp.strftime("%X"))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(mem_list[::-1])
    plt.xlabel('Data/Hora')
    plt.ylabel('Uso de memoria (MB)')
    ax.legend()
    plt.margins(0.05)
    plt.xticks(range(0, len(timestamp_list)))
    ax.set_xticklabels(timestamp_list[::-1])
    io = StringIO()
    fig.savefig(io, fortmat='png')
    graph = io.getvalue().encode('base64')
    
    return render_template("process_mem.html",
                           title='vmProcessTable {0}'.format(id),
                           data=zip(timestamp_list, mem_list),
                           graph=graph)



if __name__ == "__main__":
    connect("gerente")
    app.run('0.0.0.0', debug=True)
