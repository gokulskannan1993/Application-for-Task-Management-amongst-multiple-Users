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


class EditBoard(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # for getting current user
        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        # get the taskboard object
        tb = ndb.Key('Taskboard', int(self.request.get('key'))).get()


        # an empty list for users that are permitted in the taskboard
        permittedUsers = []


        # for showing who are the users that are allowed in the taskboard
        for email in tb.users:
            query = User.query(User.email == email).fetch()
            permittedUsers.append(query[0])



        template_values = {
            'tb': tb,
            'permittedUsers': permittedUsers,
            'noOfUsers': len(permittedUsers),
            'currentUser': currentUser
        }

        template = JINJA_ENVIRONMENT.get_template('editBoard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # get the taskboard object
        tb = ndb.Key('Taskboard', int(self.request.get('key'))).get()

        # know which button the user clicked
        action = self.request.get('button')


        # for editing the name
        if action == 'EditName':
            if self.request.get('boardName'):
                tb.name = self.request.get('boardName')
                tb.put()
            self.redirect('/editBoard?key= '+str(tb.key.id()))

        # for removing users
        elif action == 'RemoveUsers':
            selectedUsers = self.request.get('tb_user', allow_multiple=True)
            if len(selectedUsers):
                # mark the tasks Unassigned
                for user in selectedUsers:
                    for task in tb.tasks:
                        if task.user == user:
                            task.user = 'Unassigned'
                tb.put()

                # delete the board from user model
                allUsers = []
                for email in selectedUsers:
                    query = User.query(User.email == email).fetch()
                    allUsers.append(query[0])

                for user in allUsers:
                    for task in user.invitedTBs:
                        if tb.key == task:
                            user.invitedTBs.remove(task)
                user.put()


                # delete the user from board
                for user in selectedUsers:
                    for email in tb.users:
                        if email == user:
                            tb.users.remove(email)

                tb.put()

            self.redirect('/editBoard?key= '+str(tb.key.id()))
