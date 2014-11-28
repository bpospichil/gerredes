from flask import Flask, render_template
from database import ProcessTable, ProcessTableEntry
from mongoengine import connect


app = Flask(__name__)

@app.route("/vmProcessTable/")
def process_table():
    p = ProcessTable.objects.order_by('-id').first()
    return render_template("process_table.html", title='vmProcessTable', entries=p.entries)

if __name__ == "__main__":
    connect("gerente")
    app.run('0.0.0.0', debug=True)
