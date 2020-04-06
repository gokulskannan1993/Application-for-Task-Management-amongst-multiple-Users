import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from taskboard import Taskboard


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)



class AddTask(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        template_values = {
            'currentUser': currentUser,
        }

        template = JINJA_ENVIRONMENT.get_template('addTask.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        action = self.request.get("button")


        if action == "Create":
            taskboardName = self.request.get('boardName')

            tBoard = Taskboard(
                name = taskboardName,
                author = currentUser.email
            )
            tBoard.put()

            currentUser.taskBoards.append(tBoard.key)
            currentUser.put()
            self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')
