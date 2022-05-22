# Quantifier-App
Quantifier Self App using flask
The project is about developing a Quantifier App using Flask. It is used to keep track of certain
activities.Here we call these activities as trackers. Using the app, a user can signup or login to the app and set
values for these trackers along with notes. The user can edit or delete these logs or trackers.

TECHNOLOGIES USED
1.FLASK – for web framework
2.flask sqlalchemy – for querying the database
3.flask render_template , request , redirect , url_for – for rendering the html template ,getting data from
forms,redirecting to urls
4.datetime- to find live time of logging new event for trackers
5.html- create web pages

# DB SCHEMA DESIGN

# User Table Schema
      user_id Integer Primary Key, Auto Increment
      username String Unique,Not Null
      email String Unique, Not Null
      password String Unique, Not Null
# Tracker Table Schema
      tracker_id Integer Primary Key, Auto Increment
      user_id Integer ForeignKey("user.user_id"), Not Null
      name String Not Null
      tracker_type String Not Null
      description String
# Tracker_history Table Schema
      Id Integer Foreign Key("user.user_id"), Not Null
      user_id Integer Foreign Key("user.user_id"), Not Null
      tracker_id Integer Foreign Key (tracker.tracker_id), Not Null
      timestamp Integer Not Null
      value Integer Not Null
      note String
      
# FEATURES
The app has a login page and a signup page. The User has to signup, after which
the page is redirected to home page . The home page has login page hyperlink. The
user can login using email and password. The user is taken to profile page where
all the trackers created by the user is shown in tabular format. The user can add
tracker ,log a new event to already existing tracker or edit/delete the tracker
event. When clicked on the tracker name hyperlink in this table, it takes to log
details table where all log events of that tracker is shown. This can be edited or
deleted.

