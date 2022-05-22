from application.database import db

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,unique=True,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,unique=True,nullable=False)


class Tracker(db.Model):
    __tablename__='tracker'
    tracker_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    name=db.Column(db.String,nullable=False)
    tracker_type=db.Column(db.String,nullable=False)
    description=db.Column(db.String)

class Tracker_history(db.Model):
    __tablename__='tracker_history'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    tracker_id=db.Column(db.Integer,db.ForeignKey("tracker.tracker_id"),nullable=False)
    timestamp= db.Column(db.Integer,nullable=False) 
    datetime=db.Column(db.DateTime,nullable=False)
    value=db.Column(db.Integer)
    note=db.Column(db.String)
