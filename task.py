from google.appengine.ext import ndb


class Task(ndb.Model):
    title = ndb.StringProperty()
    dueDate = ndb.StringProperty()
    user = ndb.StringProperty()
    isCompleted = ndb.BooleanProperty(default=False)
