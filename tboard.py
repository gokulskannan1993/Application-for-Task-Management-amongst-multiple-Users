import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users


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


        tb = ndb.Key('Taskboard', int(self.request.get('key'))).get()




        template_values = {
            'tb': tb,

        }
        template = JINJA_ENVIRONMENT.get_template('tBoard.html')
        self.response.write(template.render(template_values))
