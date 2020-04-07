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
class UserTaskboards(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        currentTBs = []
        invitedTBs = []



        if currentUser.taskBoards:
            for keys in currentUser.taskBoards:
                taskboard = keys.get()
                currentTBs.append(taskboard)
        if currentUser.invitedTBs:
            for keys in currentUser.invitedTBs:
                taskboard = keys.get()
                invitedTBs.append(taskboard)




        template_values = {
            'currentUser': currentUser,
            'currentTBs' :currentTBs,
            'invitedTBs':invitedTBs

        }

        template = JINJA_ENVIRONMENT.get_template('userTaskboards.html')
        self.response.write(template.render(template_values))
