#!/usr/bin/env python3

import os
import sys

# Flask imports
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from flask import make_response
from flask import jsonify

# Sqlalchemy imports
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker

# Imports for oauth2 connection
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import random
import string
import httplib2
import requests

# Imports from forms module and dbsetup module
from forms import MovieForm, EditMovieForm
from dbsetup import Base, Users, Categories, Movies


app = Flask(__name__)

app.config['SECRET_KEY'] = 'e38ce1f92e4e5f3a9c0cd7ceb7cd26ca'

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Movie Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///movies.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON PUBLIC ENDPOINTS


@app.route('/home.json')
def homeJSON():
    movies = session.query(Movies).order_by(Movies.id.asc())
    # Shows all movies by movie id
    return jsonify(allMovies=[m.serialize for m in movies])


@app.route('/home.json/<int:category_id>/<int:movie_id>')
def movieByCategoryJSON(category_id, movie_id):
    movie = session.query(Movies).filter_by(id=movie_id).one()
    # Shows an arbitrary movie
    return jsonify(movie=[movie.serialize])


@app.route('/home.json/categories')
def movieCategoryJSON():
    categories = session.query(Categories).order_by(Categories.name.asc())
    # Shows all categories
    return jsonify(categories=[c.serialize for c in categories])


""" Main page - PUBLIC
Shows the last 12 added movies and a list of categories via the
dropdown menu. Clicking on an image shows the detail of the movie."""


@app.route('/')
@app.route('/home')
def home():
    pics = session.query(Movies).order_by(Movies.id.desc()).limit(12)
    categ = session.query(Categories).order_by(Categories.name.asc())
    return render_template('publicHome.html', pics=pics, categ=categ)


""" Main page - PRIVATE
Same as above, but instead of showing 12 last movies it shows all movies.
Displays add movie button. Clicking on an image shows the detail of the
movie with two more buttons (edit and delete)"""


@app.route('/private_home')
def privateHome():
    if 'username' in login_session:
        categ = session.query(Categories).order_by(Categories.name.asc())
        pics = session.query(Movies).order_by(Movies.id.desc()).all()
        return render_template('home.html', pics=pics, categ=categ)
    else:
        return redirect(url_for('home'))


""" Categories - PUBLIC AND PRIVATE
Shows movies by category after selecting a category via the dropdown
button in navbar. The function takes the category name as parameter."""


@app.route('/category/<string:movie_category>')
def category(movie_category):
    categ = session.query(Categories).order_by(Categories.name.asc())
    movie = session.query(Movies).filter_by(category=movie_category).all()
    return render_template('category.html', movie=movie, categ=categ)


""" Movie Item - PUBLIC AND PRIVATE
Shows detail of selected movie. For private users, edit and delete buttons
will display. See movieItem.html for buttons appearance. The function takes
the movie title as parameter."""


@app.route('/movieItem/<string:movie_name>/')
def movieItem(movie_name):
    categ = session.query(Categories).order_by(Categories.name.asc())
    movie = session.query(Movies).filter_by(title=movie_name).first()
    title = movie.title
    return render_template('movieItem.html', movie=movie, categ=categ,
                           login_session=login_session, title=title)


""" Add a new movie - PRIVATE
Shows a form for private users to add new movie.
- If the category doesn't exist it displays a message and doesn't add the
movie.
- If the title or cover of the movie exist it displays a message and
doesn't add the movie."""


@app.route('/addNewMovie', methods=['GET', 'POST'])
def addMovie():
    if 'username' in login_session:
        form = MovieForm()
        if form.validate_on_submit():
            # Collects data from form
            cat = form.category.data
            titl = form.title.data
            cov = form.cover.data
            # Queries for further conditional
            category = session.query(Categories).filter_by(name=cat).first()
            title = session.query(Movies).filter_by(title=titl).first()
            cover = session.query(Movies).filter_by(cover=cov).first()

            if 'username'in login_session:
                # Queries and collects the user_id from db
                user = session.query(Users).filter_by(
                    email=login_session['email']).first()
                user_id = user.id

            if request.method == 'POST':
                # Conditions for movie to be added
                if category and title is None and cover is None:
                    newMovie = Movies(title=titl, year=form.year.data,
                                      description=form.description.data,
                                      cover=cov, category=cat,
                                      category_id=category.id,
                                      user_id=user_id)
                    session.add(newMovie)
                    session.commit()
                    flash(f"The movie {titl} has been added !", 'success')
                    return redirect(url_for('privateHome'))
                elif title or cover:
                    flash('Movie already exist !', 'warning')
                    return render_template('addNewMovie.html', form=form)
                elif category is None:
                    flash(f'The category {cat} does not exist !', 'warning')
        return render_template('addNewMovie.html', form=form)
    else:
        return redirect(url_for('home'))


""" Delete a movie - PRIVATE
Displays a modal of delete confirmation. It will delete the movie only if
user id matches with movie user_id. The function takes the movie title as
parameter."""


@app.route('/deleteMovie/<string:movie_name>', methods=['GET', 'POST'])
def deleteMovie(movie_name):
    movie = session.query(Movies).filter_by(title=movie_name).first()
    title = movie.title

    if 'username' in login_session:
        user = session.query(Users).filter_by(
            email=login_session['email']).first()

        if movie.user_id == user.id:
            flash(f'The movie { title} has been removed !', 'success')
            session.delete(movie)
            session.commit()
            return redirect(url_for('privateHome'))
        else:
            flash(
                'You are not allowed to edit or delete this movie !',
                'warning')
            return redirect(url_for('movieItem', movie_name=title))


"""Edit a movie - PRIVATE
Shows a form for private users to edit or update a movie. It will allow update
only if user id matches with movie user_id. The function takes the movie
title as parameter."""


@app.route('/edit/<string:movie_name>', methods=['GET', 'POST'])
def editMovie(movie_name):
    if 'username' in login_session:
        movie = session.query(Movies).filter_by(title=movie_name).first()
        user = session.query(Users).filter_by(
            email=login_session['email']).first()
        # Here I pass the object movie (above) to prepopulate the form
        form = EditMovieForm(obj=movie)
        categ = session.query(Movies).filter_by(
            category=form.category.data).first()
        # Checks movie user_id and user id
        if movie.user_id == user.id:
            if form.validate_on_submit():
                # If conditions met apply changes
                if request.method == 'POST':
                    # Collects data from form
                    movie.title = form.title.data
                    movie.cover = form.cover.data
                    movie.year = form.year.data
                    movie.description = form.description.data

                    if categ is None:
                        flash("Category doesn't exist !", "warning")
                        return render_template('editMovie.html', form=form,
                                               movie=movie)
                    else:
                        movie.category = form.category.data

                    session.add(movie)
                    session.commit()
                    flash('Movie updated !', 'success')
                    return redirect(url_for('privateHome'))
            return render_template('editMovie.html', form=form, movie=movie)
        else:
            flash('You are not allowed to edit this movie !', 'warning')
            return redirect(url_for('movieItem', movie_name=movie.title))

    return redirect(url_for('privateHome'))


# ROUTES FOR LOGIN AND LOGOUT


"""Log in - PUBLIC
Creates the state and pass it to the login session."""


@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Log out. Logs out and flushes the login_session.


@app.route('/logout')
def logout():
    login_session.clear()
    flash('You are successfully disconnected !', 'success')
    return redirect(url_for('home'))

# Google gconnect


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
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
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current already connected.'),
                                 200)
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

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    flash(f"Welcome,  {login_session['username']}, you are now logged in !",
          'success')
    print("done!\n")

    # If user not in database, then add it.
    if 'username' in login_session:
        user = session.query(Users).filter_by(
            email=login_session['email']).first()
        if user is None:
            newUser = Users(name=login_session['username'],
                            email=login_session['email'])
            session.add(newUser)
            session.commit()
    return output


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
