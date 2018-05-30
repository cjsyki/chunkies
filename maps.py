from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import config_keys

app = Flask(__name__)

API_KEY = config_keys.MAPS

GoogleMaps(app, key = API_KEY)

@app.route('/', methods=["GET"])
def my_map():
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
    return render_template('maps.html', mymap=mymap, src = src)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)