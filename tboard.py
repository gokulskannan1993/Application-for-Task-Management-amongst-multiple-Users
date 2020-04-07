import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from user import User
from task import Task


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)


class TBoard(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        permittedUsers = []


        tb = ndb.Key('Taskboard', int(self.request.get('key'))).get()

        allUsers = User.query(User.email != currentUser.email)

        for email in tb.users:
            query = User.query(User.email == email).fetch()
            permittedUsers.append(query[0])


        template_values = {
            'tb': tb,
            'currentUser': currentUser,
            'allUsers': allUsers,
            'permittedUsers': permittedUsers

        }


        template = JINJA_ENVIRONMENT.get_template('tBoard.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')

        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        tb = ndb.Key('Taskboard', int(self.request.get('key'))).get()




        if action == 'AddUser':
            invitedUser = ndb.Key(urlsafe=(self.request.get('SelectedUser'))).get()

            if tb.key not in invitedUser.invitedTBs:
                invitedUser.invitedTBs.append(tb.key)
                tb.users.append(invitedUser.email)
                tb.put()
                invitedUser.put()
                self.redirect('/tboard?key= '+str(tb.key.id()))
            else:
                self.response.write('The selected user already has already invited')


        elif action == 'AddTask':
            taskTitle = self.request.get('taskTitle')
            dueDate = self.request.get('dueDate')
            assignedUser = self.request.get('assignedUser')

            taskTitles = []
            for task in tb.tasks:
                taskTitles.append(task.title)

            if taskTitle not in taskTitles:
                newTask = Task(
                    title = taskTitle,
                    dueDate = dueDate,
                    user = assignedUser,
                    isCompleted = False
                )
                newTask.put()

                tb.tasks.append(newTask)
                tb.put()
                self.redirect('/tboard?key= '+str(tb.key.id()))
            else:
                self.response.write('The task is already in the Taskboard')
