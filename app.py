# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
   redirect,
    request)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/db.sqlite"

db = SQLAlchemy(app)


class Gis(db.Model):
    __tablename__ = 'gisdata'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(64))
    longitude = db.Column(db.String(64))
    altitude = db.Column(db.String(64))
    time = db.Column(db.String(64))
    image=db.Column(db.String)
    comments=db.Column(db.String)

    def __repr__(self):
        return '<Gis %r>' % (self.latitude)

@app.before_first_request
def setup():
   # Recreate database each time
   db.drop_all()
   db.create_all()

# request.home['']
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        latitude = request.form["info_cur_lat"]
        longitude = request.form["info_cur_lng"]
        altitude = request.form["info_cur_alt"]
        time = request.form["info_cur_tm"]
        image=request.form["image"]
        comments=request.form["comments"]
        location = Gis(latitude=latitude, longitude=longitude, altitude=altitude, time=time,image=image,comments=comments)
        db.session.add(location)
        db.session.commit()
        
        return redirect("/", code=302)

    return render_template("home.html")

        

@app.route("/api/data")
def list_locations():
    results = db.session.query(Gis.latitude, Gis.longitude, Gis.altitude, Gis.time,Gis.image,Gis.comments).all()

    locations = []
    for result in results:
        locations.append({
            "latitude": result[0],
            "longitude": result[1],
            "altitude": result[2],
            "time": result[3],
            "image":result[4],
            "Comments":result[5]
        })
    return jsonify(locations)





if __name__ == "__main__":
   app.run(debug=True)