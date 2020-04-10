import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from datetime import datetime

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

        # for getting current user
        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        # an empty list for users that are permitted in the taskboard
        permittedUsers = []


        # gets the taskboard object
        tb = ndb.Key('Taskboard', int(self.request.get('key'))).get()

        # gets all the users except the author, used to add the user to taskboard
        allUsers = User.query(User.email != currentUser.email)

        # for showing who are the users that are allowed in the taskboard
        query = User.query(User.email == tb.author).fetch()
        permittedUsers.append(query[0])
        for email in tb.users:
            query = User.query(User.email == email).fetch()
            permittedUsers.append(query[0])



        # for displaying counters
        totalTasks = len(tb.tasks)
        pendingTasks = 0
        completedTasks = 0
        completedToday = 0

        # get todays date
        today = datetime.now().strftime("%d/%m/%Y")


        for task in tb.tasks:
            if task.isCompleted:
                completedTasks+=1
                completedDate = task.completedOn.split(" ")[0]
                if completedDate == today:
                    completedToday +=1
            else:
                pendingTasks+=1







        template_values = {
            'tb': tb,
            'currentUser': currentUser,
            'allUsers': allUsers,
            'permittedUsers': permittedUsers,
            'totalTasks': totalTasks,
            'pendingTasks': pendingTasks,
            'completedTasks': completedTasks,
            'completedToday': completedToday

        }


        template = JINJA_ENVIRONMENT.get_template('tBoard.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # know which button the user clicked
        action = self.request.get('button')

        # for getting current user
        user = users.get_current_user()
        userKey = ndb.Key('User',user.user_id())
        currentUser = userKey.get()

        # gets the taskboard object
        tb = ndb.Key('Taskboard', int(self.request.get('key'))).get()




        # if the user is the author and wants to invite another user
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


        # if the user wants to add a task
        elif action == 'AddTask':
            taskTitle = self.request.get('taskTitle')
            dueDate = self.request.get('dueDate')
            assignedUser = self.request.get('assignedUser')


            # get all the task titles to make sure it is not already in the board
            taskTitles = []
            for task in tb.tasks:
                taskTitles.append(task.title)

            # checking for the task with the same name
            if taskTitle not in taskTitles:
                # create a new Task object
                newTask = Task(
                    title = taskTitle,
                    dueDate = dueDate,
                    user = assignedUser,
                    isCompleted = False
                )

                # add the task to the board
                tb.tasks.append(newTask)
                tb.put()
                self.redirect('/tboard?key= '+str(tb.key.id()))
            else:
                self.response.write('The task is already in the Taskboard')


        # to mark the task completed
        elif action == 'MarkCompleted':
            marked = self.request.get('isCompleted', allow_multiple = True)

            for index in marked:
                tb.tasks[int(index)].isCompleted = True
                tb.tasks[int(index)].completedOn = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tb.put()
            self.redirect('/tboard?key= '+str(tb.key.id()))

        # to delete taskboard
        elif action == 'DeleteTaskboard':

            totalUsers = len(tb.users)
            totalTasks = len(tb.tasks)
            if totalUsers == 0 and totalTasks == 0:
                for key in currentUser.taskBoards:
                    if tb.key == key:
                        currentUser.taskBoards.remove(key)
                currentUser.put()
                tb.key.delete()
                self.redirect('/userTaskboards')
            else:
                self.response.write('The board cannot be deleted as it still has members or tasks')
