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

API_KEY = config_keys.MAPS
GoogleMaps(app, key = API_KEY)

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm( )
    if form.validate_on_submit( ):
        zipcode = form.zipcode.data
        option = form.options.data
        businessesDict = yelp.query_api(option, str(zipcode))
        global business_id_array
        business_id_array = []
        retString = ""
        for i in range(0, len(businessesDict)):
            business_id = businessesDict[i]['id']
            business_id_array.append(business_id)
        random.shuffle(business_id_array)
        print(business_id_array)
        return pickRestaurant()
        # return redirect(url_for('results'))
    return render_template("search.html", form=form)

business_id_array = []
current_id_pos = 0
def pickRestaurant():
    global current_id_pos
    business_id = business_id_array[current_id_pos]
    current_id_pos += 1
    print(current_id_pos)
    return redirect(url_for("results", id = business_id))

# creates the map, utilizes api key, and returns template
@app.route('/results/<id>', methods=['GET', 'POST'])
@login_required
def results(id):
    restaurant = yelp.get_business(yelp.API_KEY, id)
    print(restaurant)
    coordinates = restaurantMethods.returnCoordinates(restaurant)
    lat = coordinates[0]
    lng = coordinates[1]
    print(lat, lng)
    src = "https://maps.googleapis.com/maps/api/js?key=%s&callback=initMap" %API_KEY
    form = ResultsForm()
    if form.is_submitted():
        return pickRestaurant()
    return render_template('results.html', form=form, src=src, lat=lat, lng=lng)

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            # flash('Invalid username or password')
            return redirect(url_for('login'))
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
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    return render_template('index.html')