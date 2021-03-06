import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images

from user import User


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join( os.path.dirname(__file__), 'views')),
    extensions = [ 'jinja2.ext.autoescape' ],
    autoescape = True
)

class ViewAllCommentsInAPost(webapp2.RequestHandler):
    def get(self, post_id):
        url = ''
        my_user = None
        user = users.get_current_user()
        fullname = ""
        username = ""

        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        else:
            url = users.create_logout_url( self.request.uri )
            my_user_key = ndb.Key('User', user.user_id())
            my_user = my_user_key.get()

            if my_user == None:
                my_user = User(id=user.user_id())
                my_user.put()
                self.redirect('/update-profile')
                return
            else:
                if my_user.lastname and my_user.lastname:
                    fullname = str(my_user.firstname).capitalize() + " " + str(my_user.lastname).capitalize()
                    username = str(my_user.username).lower()
                else:
                    self.redirect('/update-profile')
                    return

        post = ndb.Key( 'Post', int(post_id) ).get()

        template_values = {
            "url": url,
            "fullname": fullname,
            "username": username,
            "comments": reversed(post.comments)
        }
        template = JINJA_ENVIRONMENT.get_template('view_all_comments.html')
        self.response.write(template.render(template_values))
        return
