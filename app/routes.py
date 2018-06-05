import yelp
import random
import config_keys
import restaurantMethods
from app import app, db
from app.models import User
from flask_googlemaps import Map, GoogleMaps
from app.forms import LoginForm, RegistrationForm, SearchForm
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
        business_id_array = []
        retString = ""
        for i in range(0, len(businessesDict)):
            business_id = businessesDict[i]['id']
            print(business_id)
            business_id_array.append(business_id)
        random.shuffle(business_id_array)
        for i in range(0, len(business_id_array)):
            restaurant = yelp.get_business(yelp.API_KEY, business_id_array[i])
            retString += restaurant['name'] + "<br>"
        return retString
        # return redirect(url_for('results'))
    return render_template("search.html", form=form)

# creates the map, utilizes api key, and returns template
@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    # return yelp.
    mymap = Map(
                identifier="view-side",
                varname="mymap",
                style="height:720px;width:1100px;margin:0;", # hardcoded!
                lat=37.4419, # hardcoded!
                lng=-122.1419, # hardcoded!
                zoom=15,
                markers=[(37.4419, -122.1419)] # hardcoded!
            )
    src = "https://maps.googleapis.com/maps/api/js?key=%s&callback=initMap" %API_KEY
    return render_template('results.html', mymap=mymap, src=src)

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
    return render_template('index.html')
