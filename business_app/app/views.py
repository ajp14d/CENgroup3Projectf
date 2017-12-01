from app import b_app
from app.database import userAcct, usrAgenda, getAgenda
import requests
import re
import shelve
from flask import render_template, request, make_response, redirect, url_for

loggedIn = False
currUser = ""
email = ""

@b_app.context_processor
def addUser():
  return dict(acct=currUser)

#Route for the index or home page
@b_app.route('/', methods=['GET', 'POST'])
def home():
    pw = ""
    acct = ""
    err = ""
    print "in register"
    print (request.method)

    #if the user is logged in, do not allow them to go back to register
    print currUser
    if currUser != "":
        return redirect(url_for('index'))

    print(request.method)
    if request.method == 'POST':
        #if the sign in button was pressed
        data = request.form['signSubmit']
        if request.form['signSubmit'] == 'submitted':
            s = shelve.open('acct.db')	#open the database
            #check if the account has been created, where user_key is the email
            try:
                print("trying...")
                if str(request.form.get('user_key')) in s:
                    #check to see if password matches the user's actual password
                    if s[str(request.form.get('user_key'))]['password'] == str(request.form.get('user_password')):
                        loggedIn = True
                        currUser = s[str(request.form.get('user_key'))]['name']
                        email = str(request.form.get('user_key'))
                        return redirect(url_for('index'))
					#if not failure, display output
                    else:
                        pw = "Invalid credentials. Incorrect password or email."
                        return render_template('register.html', pw=pw)
                else:
                    pw = "User account is not registered."
                    return render_template('register.html', pw=pw)

            except KeyError:
				print "Account not registered"
        elif request.form['signSubmit'] == 'signUpSubmit':
            print("in signup")
            #get the name, acct, password for the user when they sign up
            name = str(request.form.get('username'))
            acct = str(request.form.get('useremail'))
            pw = str(request.form.get('userpass'))
            #store it in the database if successful
            message = userAcct(name, acct, pw)
            #if the database returns a failure
            if message == 'failure':
                err = "Email is already taken. Please try again"
                return render_template("register.html", err=err)
            #check for a valid email format
            elif re.search("@([0-9a-z][0-9a-z-]+.)+[a-z]{2,4}$", acct) is None:
                err = "Please enter a valid email address"
                print "Invalid Email Format"
                return render_template("register.html", err=err)
            elif len(pw) < 7:
                err = "Password is too short (minimum of 7 characters)"
                print "short password"
                return render_template("register.html", err=err)
            #if no error take them to index page
            else:
                err = ""
                loggedIn = True
                global currUser
                currUser = name
                global email
                email = acct
                return redirect(url_for('index'))


    #create the view for register.html
    return render_template('register.html', err=err)

@b_app.route('/index.html', methods=['GET', 'POST'])
def index():
    if currUser == "":
        return redirect(url_for('home'))

    #create the view for the index
    return render_template('index.html')

@b_app.route('/clothing.html')
def signup():
    if currUser == "":
        return redirect(url_for('home'))

    return render_template('clothing.html')

@b_app.route('/agenda.html', methods=['GET', 'POST'])
def newthing():
    if currUser == "":
        return redirect(url_for('home'))

    print "in agenda"
    print (request.method)
    info = None

    if request.method == 'POST':
        eventName = request.form.get('eventName')
        eventType = request.form.get('eventType')
        compName = request.form.get('companyname')
        attire = request.form.get('attire')
        additional = request.form.get('info')

        alert = usrAgenda(email, eventName, eventType, compName, attire, additional)
        return redirect(url_for('profile', alert=alert))


    return render_template('agenda.html')

@b_app.route('/interviewQA.html')
def newinterview():
    if currUser == "":
        return redirect(url_for('home'))

    return render_template('interviewQA.html')

@b_app.route('/Calendar.html')
def newdate():
    if currUser == "":
        return redirect(url_for('home'))

    return render_template('Calendar.html')

@b_app.route('/about.html')
def aboutus():
    if currUser == "": 
        return redirect(url_for('home'))

    return render_template('about.html')

@b_app.route('/signout.html')
def signout():
    global currUser
    currUser = ""
    if currUser == "":
        return redirect(url_for('home'))

    return render_template('signout.html')

@b_app.route('/profile.html')
def profile():
    print currUser
    if currUser == "":
        return redirect(url_for('home'))

    agenda = getAgenda(email)
    return render_template('profile.html', agenda=agenda)
