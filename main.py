import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from user import User
from addTask import AddTask
from tboard import TBoard
from userTaskboards import UserTaskboards

from editTask import EditTask

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        user = users.get_current_user()


        # initializing the strings and values
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        currentUser = None





        # determine if we have a user logged in or not.
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            username = user.email().split("@")[0]


            userKey = ndb.Key('User',user.user_id())
            currentUser = userKey.get()


            if currentUser == None:
                welcome = 'Welcome to the application'
                myuser = User(
                    id = user.user_id(),
                    email = user.email(),
                    name = username
                     )
                myuser.put()
                userKey = ndb.Key('User',user.user_id())
                currentUser = userKey.get()




        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome': welcome,
            'currentUser':currentUser,

        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))



app = webapp2.WSGIApplication(
            [
            ('/', MainPage),
            ('/addtask', AddTask),
            ('/tboard', TBoard),
            ('/userTaskboards', UserTaskboards),
            ('/editTask', EditTask)

            ],
            debug = True
        )
