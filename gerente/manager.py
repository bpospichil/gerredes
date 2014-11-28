from flask import Flask
from snimpy.manager import Manager, load

app = Flask(__name__)
load("SNMPv2-MIB")
host = "104.131.91.218"
community = "vlavaav"
m = Manager(host, community);

@app.route("/")
def hello():
    return m.sysDescr

if __name__ == "__main__":
    app.run('0.0.0.0')
