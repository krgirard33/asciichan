#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

'''USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")'''

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        templ = jinja_env.get_template(template)
        return templ.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    """ Handles the main function of making front and getting submits """

    def render_front(self, title="", art="", error=""):
        """ handles all drawing of front.html """

        arts = db.GqlQuery("SELECT * FROM Art "
                            "ORDER BY created DESC ")
        self.render("front.html", title=title, art=art, error=error, arts=arts)


    def get(self):
        """ Creates the front page """
        #self.write("Word")
        # items = self.request.get_all("food")
        self.render_front()

    def post(self):
        """ gets the title and artwork """
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title=title, art=art)
            a.put()

            self.redirect("/")
        else:
            error = "we need both a title and some artwork"
            self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
