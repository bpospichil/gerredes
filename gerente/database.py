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

class ProcessCount(Document):
    value = IntField()
    timestamp = DateTimeField(default = datetime.datetime.now)

class VideoTableEntry(EmbeddedDocument):
    index = IntField(required=True)
    ident = IntField(required=True)
    audience = IntField()
    advertising = IntField()
    vod = IntField()
    live = IntField()

class VideoTable(Document):
    entries = ListField(EmbeddedDocumentField(VideoTableEntry))
    timestamp = DateTimeField(default = datetime.datetime.now)
   
