import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from user import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)


class EditTask(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # for getting current user
        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        # gets the taskboard object
        tb = ndb.Key('Taskboard', int(self.request.get('tbKey'))).get()

        # get the loop index
        index = int(self.request.get('task'))


        # an empty list for users that are permitted in the taskboard
        permittedUsers = []
        # for showing who are the users that are allowed in the taskboard
        query = User.query(User.email == tb.author).fetch()
        permittedUsers.append(query[0])
        for email in tb.users:
            query = User.query(User.email == email).fetch()
            permittedUsers.append(query[0])



        template_values = {
            'taskboard': tb,
            'task': tb.tasks[index],
            'permittedUsers':permittedUsers,
            'index':index
        }

        template = JINJA_ENVIRONMENT.get_template('editTask.html')
        self.response.write(template.render(template_values))




    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # for getting current user
        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        # gets the taskboard object
        tb = ndb.Key('Taskboard', int(self.request.get('tbKey'))).get()

        # get the loop index
        index = int(self.request.get('task'))


        # get the button value
        action = self.request.get('button')


        # if the user wants to edit
        if action == 'Edit':
            tb.tasks[index].user = self.request.get('task_assigned')
            tb.tasks[index].dueDate = self.request.get('task_due_date')
            tb.tasks[index].title = self.request.get('task_title')
            tb.tasks[index].isCompleted = False
            tb.put()
            self.redirect('/tboard?key='+str(tb.key.id()))
        # elif the user wants to delete
        elif action == 'Delete':
            del tb.tasks[index]
            tb.put()
            self.redirect('/tboard?key='+str(tb.key.id()))

        # elif the user wants to cancel the operation
        elif action == 'Cancel':
            self.redirect('/tboard?key='+str(tb.key.id()))
