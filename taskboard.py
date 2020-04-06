from google.appengine.ext import ndb
from task import Task

class Taskboard(ndb.Model):
    name = ndb.StringProperty()
    tasks = ndb.StructuredProperty(Task, repeated = True)
    author = ndb.StringProperty()
    users = ndb.StringProperty(repeated=True)
