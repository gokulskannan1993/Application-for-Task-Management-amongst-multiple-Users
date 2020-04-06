from google.appengine.ext import ndb
from taskboard import Taskboard

class User(ndb.Model):
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    taskBoards = ndb.KeyProperty(Taskboard, repeated = True)
    invitedTBs = ndb.KeyProperty(Taskboard,repeated=True)
