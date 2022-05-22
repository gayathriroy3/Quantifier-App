from flask import Flask,request
from flask import render_template
from flask import current_app as app
from application.database import db
from application.models import User,Tracker_history,Tracker
from flask import request,redirect,url_for,session
import matplotlib.pyplot as plt
from datetime import datetime
import os

@app.route("/",methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user_details=User.query.filter_by(email=email).first()
        session["name"] = user_details.username
        session['id']=user_details.user_id
        return redirect(url_for('profile'))
        
    return render_template("login.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.form['email']
        username=request.form['name']
        password=request.form['password']
        user = User(email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
        
    return render_template("signup.html")




@app.route('/profile',methods=['GET','POST'])
def profile():
    user=User.query.filter_by(user_id=session['id']).first()
    trackers=Tracker.query.filter_by(user_id=user.user_id).all()
    if trackers!=None:
        timestamps=[]
        for tracker in trackers:
            timestampx=[]
            tracker_history=Tracker_history.query.filter_by(tracker_id=tracker.tracker_id).all()
            
            for t in tracker_history:
                
                timestampx.append((t.timestamp,t.datetime))
            timestampx.sort()
            
            if len(timestampx)!=0:
                timestamps.append(timestampx[-1])
            else:
                timestamps.append(0) 
        return render_template('profile.html',trackers=trackers,timestamps=timestamps,user_id=user.user_id)
    else:
        return render_template('profile.html',user_id=user.user_id)
   

@app.route("/profile/create/<int:user_id>",methods=['GET','POST'])
def create_tracker(user_id):
    
    if request.method=='POST':
        name=request.form['name']
        tracker_type=request.form['type']
        description=request.form['description']
        track_exist=Tracker.query.filter_by(name=name,user_id=user_id).first()
        if track_exist!=None:
                return render_template("create.html",act=1)
        else:
            tracker = Tracker(name=name,tracker_type=tracker_type,description=description,user_id=user_id,)
            db.session.add(tracker)
            db.session.commit()
            return redirect('/profile')

    return render_template("create.html",user_id=user_id)

@app.route("/tracker/new-event/<int:user_id>/<int:tracker_id>",methods=['GET','POST'])
def new_event(user_id,tracker_id):
    if request.method=='POST':
        value=request.form['value']
        note=request.form['note']
        dt = datetime.now()
        
        ts = datetime.timestamp(dt)

        tracker_history=Tracker_history(user_id=user_id,tracker_id=tracker_id,value=value,note=note,timestamp=ts,datetime=dt)
        db.session.add(tracker_history)
        db.session.commit()
        return redirect('/profile')
    return render_template("new_event.html",user_id=user_id,tracker_id=tracker_id)

@app.route("/tracker/<int:user_id>/<int:tracker_id>/edit",methods=['GET','POST'])
def edit_tracker(user_id,tracker_id):
    tracker=Tracker.query.filter_by(user_id=user_id,tracker_id=tracker_id).first()
    if request.method=='POST':
        name=request.form['name']
        description=request.form['description']
        tracker=Tracker.query.filter_by(user_id=user_id,tracker_id=tracker_id).first()
        if tracker.name==name:
            return render_template("edit_tracker.html",act=1)
        tracker.name=name
        tracker.description= description
        db.session.commit()
        return redirect('/profile')
    return render_template("edit_tracker.html",user_id=user_id,tracker_id=tracker_id,tracker_type=tracker.tracker_type)


@app.route("/tracker/<int:user_id>/<int:tracker_id>/delete",methods=['GET','POST'])
def delete_tracker(user_id,tracker_id):
    tracker = Tracker.query.filter_by(user_id=user_id,tracker_id=tracker_id).first()
    tracker_histories = Tracker_history.query.filter_by(user_id=user_id,tracker_id=tracker_id).all()
    db.session.delete(tracker)
    for tracker_history in tracker_histories:
        db.session.delete(tracker_history)
    db.session.commit()
    return redirect('/profile')
    

@app.route("/tracker/<int:user_id>/<int:tracker_id>/log_details",methods=['GET','POST'])
def log_details(user_id,tracker_id):
    tracker_histories=Tracker_history.query.filter_by(user_id=user_id,tracker_id=tracker_id).all()
    timestamps=[]
    value=[]
    for tracker_history in tracker_histories:
        timestamps.append(tracker_history.datetime)
        value.append(tracker_history.value)

    from os.path import exists
    file_exists = exists('static/my_plot.png')
    print(file_exists)
    if file_exists:
        os.remove(r'static/my_plot.png')
    plt.plot(timestamps, value)
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.savefig('static/my_plot.png')
    
    
    
    return render_template("log_details.html",user_id=user_id,tracker_id=tracker_id,tracker_histories=tracker_histories)

@app.route("/tracker_history/<int:user_id>/<int:tracker_id>/edit",methods=['GET','POST'])
def edit_log_details(user_id,tracker_id):
    tracker_history=Tracker_history.query.filter_by(user_id=user_id,tracker_id=tracker_id).first()
    if request.method=='POST':
        value=request.form['value']
        note=request.form['note']
        tracker_history.value=value
        tracker_history.note=note
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        tracker_history.timestamp=ts
        db.session.commit()
        return redirect("/profile")
    return render_template("edit_log_details.html",user_id=user_id,tracker_id=tracker_id,tracker_history=tracker_history)

@app.route("/tracker_history/<int:user_id>/<int:tracker_id>/delete",methods=['GET','POST'])
def delete_log_details(user_id,tracker_id):
    tracker_history=Tracker_history.query.filter_by(user_id=user_id,tracker_id=tracker_id).first()
    if tracker_history is not None:
        db.session.delete(tracker_history)
        db.session.commit()
        return redirect("/profile")



@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

