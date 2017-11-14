# using python 3

'''
TO DO:



-- better UX on login

-- Make sure everything is mobile responsive, relatively. should work well on a mobile phone






'''

from datetime import datetime
from models import Base, User, Entry
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import desc
from flask.ext.httpauth import HTTPBasicAuth
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import sys
from flask import make_response
import requests
from functools import wraps

try:
    if sys.argv[1] == 'dev':
        dbpath = 'sqlite:///bodytalkdev3.db'
    elif sys.argv[1] == 'dep':
        dbpath = 'postgresql://bodytalk:password@localhost/bodytalk'
except:
    if __name__ != '__main__': #if being called by wsgi/apache
        dbpath = 'postgresql://bodytalk:password@localhost/bodytalk'
# else:
#     dbpath = 'sqlite:///bodytalkdev3.db'


maxItems = 50 #max number of items on any one page

auth = HTTPBasicAuth()

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

CLIENT_ID = json.loads(open(dir_path + '/' +  'client_secrets.json', 'r').read())[
    'web']['client_id']

engine = create_engine(dbpath)
Base.metadata.create_all(engine)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)
app.secret_key = "super secret key"

'''


'''
categories = ['visions', 'sounds', 'odors', 'feelings', 'tastes']

# helper functions

def getItems():
    items = session.query(Entry).all()
    return items


def check_authorized():
    if 'username' in login_session:
        return True
    else:
        return False


@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
    '''
    authenticates the user with Google+
    '''
    items = getItems()
    if request.method == 'GET':
        return render_template('main.html', email=login_session['email'],
                               flash='welcome, ' + login_session['name'],
                               authorized=True,
                               categories=categories, items=items)
    if request.method == 'POST':
        # Validate state token
        if request.args.get('state') != login_session['state']:
            response = make_response(json.dumps(
                'Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        # Obtain authorization code
        code = request.data

        try:
            # Upgrade the authorization code into a credentials object
            # oauth_flow = flow_from_clientsecrets(
            #     '/var/www/bodytalk/bodytalk/client_secrets.json', scope='')
            dir_path = os.path.dirname(os.path.realpath(__file__))
            oauth_flow = flow_from_clientsecrets(
                dir_path + '/' + 'client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(code)
        except FlowExchangeError:
            response = make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        print(access_token)
        sys.stderr.write(access_token)
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is used for the intended user.
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            response = make_response(
                json.dumps("Token's user ID doesn't match user ID."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is valid for this app.
        if result['issued_to'] != CLIENT_ID:
            response = make_response(
                json.dumps("Token's client ID does not match app's."), 401)
            print("Token's client ID does not match app's.")
            response.headers['Content-Type'] = 'application/json'
            return response

        # Store the access token in the session for later use.
        login_session['access_token'] = credentials.access_token
        login_session['gplus_id'] = gplus_id

        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']
        login_session['name'] = data['given_name']

        print(data)

        return 'hellow mor'


@app.route('/gdisconnect')
def gdisconnect():
    ''' 
    logout 
    '''
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200' or '400':
        name = login_session['name']
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['name']
        return render_template('main.html', authorized=False,
                               items=getItems(), categories=categories)
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/login')
def showLogin():
    '''
    show a login button
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(0, 32))
    login_session['state'] = state
    return render_template('login.html', STATE=login_session['state'],
                           items=getItems(), categories=categories)


@app.route('/')
def homePage():

    authorized = check_authorized()
   
    if 'email' in login_session:
        email = login_session['email']
    else:
        email = None

    # items = session.query(Entry).all()
    items = session.query(Entry).order_by(desc(Entry.time)).limit(maxItems).all()
    # for i in items:
    #     if i.category=="touching":
    #         i.category="feeling the touch of"
    return render_template('main.html', categories=categories,
                           items=items, authorized=authorized, email=email, add=True)


@app.route('/item/<itemID>')
def showItem(itemID):
    ''' 
    return a page describing an item given its id
    '''
    item = session.query(Entry).filter_by(id=itemID).one()

    items = session.query(Entry).all()

    authorized = check_authorized()

    if 'email' in login_session:
        if item.creatorEmail == login_session['email'] or login_session['email']=='dane.email@gmail.com':
            permitted = True
            email = login_session['email']
        else:
            permitted = False
            email = None
    else:
        permitted = False
        email = None

    return render_template('item.html', item=item, category=item.category,
                           categories=categories,
                           authorized=authorized,
                           permitted=permitted, email = email)


@app.route('/delete/<itemID>')
def confirmDelete(itemID):
    item = session.query(Entry).filter_by(id=itemID).one()

    items = session.query(Entry).all()

    authorized = check_authorized()

    return render_template('deleteItem.html', item=item,
                           categories=categories, authorized=authorized)


@app.route('/add', methods=['GET', 'POST'])
def add():
    '''
    check if a user is logged in;
    if logged in, show the add item page
    '''
    if request.method == 'POST':

        authorized = check_authorized()

        if authorized:
            category = request.form['category']
            # word = request.form['word'].lower()
            entry = request.form['entry'].lower()

            newWord = Entry(entry = entry,
                            category=category,
                            time = datetime.now(),
                            creatorEmail=login_session['email'])
            session.add(newWord)
            session.commit()

        items = session.query(Entry).all()

        if 'email' in login_session:
            email = login_session['email']

        return redirect('/')
    if request.method == 'GET':
        # items = session.query(Entry).all()

        authorized = check_authorized()

        if 'email' in login_session:
            email = login_session['email']

        return render_template('addItem.html',
                               categories=categories,
                               authorized=True, email=email)


@app.route('/edit/<itemID>', methods=['GET', 'POST'])
def edit(itemID):
    if request.method == 'POST':

        authorized = check_authorized()

        word = session.query(Entry).filter_by(id=itemID).one()

        if word.creatorEmail == login_session['email']:
            if request.form['word'] != "":
                word.word = request.form['word'].lower()

            word.category = request.form['category']

            if request.form['entry'] != "":
                word.definition = request.form['entry'].lower()

            session.add(word)
            session.commit()

        else:
            print('no match')
            print(word.creatorEmail)
            print(login_session['email'])

        items = session.query(Entry).all()

        return render_template('main.html', categories=categories,
                               items=items, authorized=authorized)

    if request.method == 'GET':
        item = session.query(Entry).filter_by(id=itemID).one()
        items = session.query(Entry).all()

        authorized = check_authorized()
        return render_template('editItem.html', item=item,
                               categories=categories, authorized=authorized)


@app.route('/fetch/<word>')
def fetchOne(word):
    '''
    json endpoint for a given word
    '''
    try:
        word = session.query(Entry).filter_by(word=word).one()
        return jsonify(word.serialize)
    except:
        return "that word couldn't be located in our database."


@app.route('/fetch')
def fetchAll():
    '''
    json endpoint for the entire database
    '''
    all = session.query(Entry).all()
    dump = []
    for i in all:
        dump.append(i.serialize)

    return jsonify(dump)


@app.route('/d/<itemID>')
def deleteItem(itemID):

    authorized = check_authorized()

    try:
        d = session.query(Entry).filter_by(id=itemID).one()
        if d.creatorEmail == login_session['email'] or login_session['email'] == 'dane.email@gmail.com':
            session.delete(d)
            session.commit()
    except:
        items = session.query(Entry).all()

        authorized = check_authorized()

        return render_template('main.html', categories=categories,
                               items=items, authorized=authorized)

    items = session.query(Entry).all()

    return redirect('/')


@app.route('/user/<user>')
def userPage(user):
    if login_session['email'] != user + "@gmail.com":
        return redirect("/", code=302)
    
    authorized = check_authorized()
    # return render_template('user.html', user)
    items = session.query(Entry).filter_by(creatorEmail=login_session['email']).order_by(desc(Entry.time)).all()

    today = []
    yesterday = []
    sevendays = []
    thirtydays = []
    ninetydays = []
    oneyear = []
    twoyears = []
    threeyears = []
    fouryears = []
    fiveyears = []

    now = datetime.now()
    for item in items:
        delta = now - item.time
        if delta.days<1:
            today.append(item)
        elif delta.days<2:
            yesterday.append(item)
        elif delta.days<7:
            sevendays.append(item)
        elif delta.days<30:
            thirtydays.append(item)
        elif delta.days<90:
            ninetydays.append(item)
        elif delta.days<365:
            oneyear.append(item)
        elif delta.days<365*2:
            twoyears.append(item)
        elif delta.days<365*3:
            threeyears.append(item)
        elif delta.days<365*4:
            fouryears.append(item)
        elif delta.days<365*5:
            fiveyears.append(item)


    return render_template('user.html', categories=categories, category="user",
                           items=items, authorized=authorized, email=login_session['email'],
                           today = today,
                           yesterday = yesterday,
                           sevendays = sevendays,
                           thirtydays = thirtydays,
                           ninetydays = ninetydays,
                           oneyear = oneyear,
                           twoyears = twoyears,
                           threeyears = threeyears,
                           fouryears = fouryears,
                           fiveyears = fiveyears)


@app.route('/category/<category>')
def revealCategory(category):

    authorized = check_authorized()

    items = session.query(Entry).all()

    filteredItems = session.query(Entry).filter_by(category=category)

    if 'email' in login_session:
        email = login_session['email']
    else:
        email = None

    return render_template('category.html', categories=categories,
                           category=category, items=filteredItems,
                           authorized=authorized, email=email)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
