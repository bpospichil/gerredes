from mongoengine import *
import datetime

class ProcessTableEntry(EmbeddedDocument):
    index = IntField(required=True)
    pid = IntField(required=True)
    owner = StringField(required=False)
    cpu = IntField()
    mem = IntField()
    state = StringField(max_length=5, required=False)

class ProcessTable(Document):
    entries = ListField(EmbeddedDocumentField(ProcessTableEntry))
    timestamp = DateTimeField(default = datetime.datetime.now)
   
class UptimeScalar(Document):
    value = IntField()
    timestamp = DateTimeField(default = datetime.datetime.now)

