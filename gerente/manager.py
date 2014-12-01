from flask import Flask, render_template, abort, request, flash, redirect, url_for, request, Response
from database import ProcessTable, ProcessTableEntry, UptimeScalar, ProcessCount, VideoTable, VideoTableEntry
from mongoengine import connect
from functools import wraps


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO

import time

app = Flask(__name__)
app.secret_key = 'vlavaav'

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def gen_graph(kind, xvals, yvals, xlabel, ylabel):
    if len(xvals) > 10:
        xvals = xvals[:10]
    if len(yvals) > 10:
        yvals = yvals[:10]

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

@app.route("/")
@requires_auth
def root():
    return redirect(url_for('uptime'))


@app.route("/vmUptime/")
@requires_auth
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
                           value=time.strftime('%X', time.gmtime(int(last.value))),
                           maxvalue=time.strftime('%X', time.gmtime(maxuptime)),
                           kind='Uptime',
                           has_set=False)


@app.route("/vmProcessTable/")
@requires_auth
def process_table():
    p = ProcessTable.objects.order_by('-id').first()
    return render_template("process_table.html", 
		           title='vmProcessTable',
                           entries=p.entries, 
                           date=p.timestamp.strftime("%x - %X"))

@app.route("/vmProcessMem/<int:id>")
@requires_auth
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
@requires_auth
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

@app.route("/vmProcessCount/", methods=['GET', 'POST'])
@requires_auth
def process_count():
    objs = ProcessCount.objects.all()
    last = objs.order_by('-id').first()

    if request.method == 'GET':    
        return render_template('scalar.html',
                               title='vmProcessCount.0',
                               date=last.timestamp.strftime("%x - %X"),
                               value=last.value,
                               maxvalue=0,
                               kind='Numero de processos',
                               has_set=True)
    if request.method == 'POST':
        value = int(request.form['newvalue'])
        if value != last.value:
            p = ProcessCount(value=value)
            p.save()
            flash('Registro atualizado com sucesso')
            return redirect(url_for('process_count'))


@app.route("/vmVideoTable/")
@requires_auth
def video_table():
    p = VideoTable.objects.order_by('-id').first()
    return render_template("video_table.html", 
		           title='vmVideoTable',
                           entries=p.entries, 
                           date=p.timestamp.strftime("%x - %X"))

@app.route("/vmVideoAdvertisingMetrics/<int:idx>")
@requires_auth
def video_advertising(idx):
    objs = VideoTable.objects.all()
    last = objs.order_by('-id').first()
    advertising = 0
    for entry in last.entries:
        if entry.index == idx:
             advertising = entry.advertising
    if request.method == 'GET':    
        return render_template('scalar.html',
                               title='vmVideoAdvertisingMetrics.{}'.format(idx),
                               date=last.timestamp.strftime("%x - %X"),
                               value=advertising,
                               maxvalue=0,
                               kind='Frequencia de propaganda',
                               has_set=True)

if __name__ == "__main__":
    connect("gerente")
    app.run('0.0.0.0', debug=True)
