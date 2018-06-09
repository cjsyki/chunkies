import yelp
import random
import config_keys
import restaurantMethods
from app import app, db
from app.models import User
from flask_googlemaps import Map, GoogleMaps
from app.forms import LoginForm, RegistrationForm, SearchForm, ResultsForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user

# keys
API_KEY = config_keys.MAPS
GoogleMaps(app, key = API_KEY)

# global variables
business_id_array = []
current_id_pos = 0

# webform to search for restaurants 
@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm( )
    # if form is submitted, take zip code and option user gave
    # feed it to yelp api to get a json file back
    if form.validate_on_submit( ):
        zipcode = form.zipcode.data
        option = form.options.data
        businessesDict = yelp.query_api(option, str(zipcode))
        # from json file, take each elements id and append it to THE GLOBAL ARRAY
        # shuffle GLOBAL ARRAY and return helper function
        global business_id_array
        for i in range(0, len(businessesDict)):
            business_id = businessesDict[i]['id']
            business_id_array.append(business_id)
        random.shuffle(business_id_array)
        # print(business_id_array)
        return pickRestaurant()
    # else, return template
    return render_template("search.html", form=form)

# takes the global array (NOW FILLED BC ITS CALLED BY SEARCH FUNCTION)
def pickRestaurant():
    # globalize current_id_pos to be modified
    # if this is the first call of function, var = 0
    # use it as index of global array to grab a single id
    # and increment global var
    global current_id_pos
    business_id = business_id_array[current_id_pos]
    current_id_pos += 1
    print(current_id_pos)
    # return results html w the single id
    return redirect(url_for("results", id = business_id))

# results page
@app.route('/results/<id>', methods=['GET', 'POST'])
@login_required
def results(id):
    if current_id_pos == 0:
        return redirect(url_for('search'))
    # given id, get corresponding restaurant to id
    restaurant = yelp.get_business(yelp.API_KEY, id)
    print(restaurant)
    # get coordinates of restaurant, and pass it onto map
    coordinates = restaurantMethods.returnCoordinates(restaurant)
    lat = coordinates[0]
    lng = coordinates[1]
    print(lat, lng)
    # api key attached to source
    src = "https://maps.googleapis.com/maps/api/js?key=%s&callback=initMap" %API_KEY
    form = ResultsForm()
    # if "click here for another restaurant" is clicked
    # return the helper function to generate anotehr id
    if form.is_submitted():
        return pickRestaurant()
    # else return html
    return render_template('results.html', form=form, src=src, lat=lat, lng=lng)

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, return search
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if email does not exist or password is wrong,
        # give error
        if user is None or not user.check_password(form.password.data):
            # flash('Invalid username or password')
            return redirect(url_for('login'))
        # else, login the user and redirect
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('search'))
    return render_template('login.html', form=form)

# logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # take users email and password, and bring it to database
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# homepage/index
@app.route('/index')
@app.route('/')
def index():
    # homepage
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    return render_template('index.html')