import os
from flask import Flask, Response, render_template, send_file, request
from flask.ext.sqlalchemy import SQLAlchemy
from tempfile import NamedTemporaryFile
import random

from lib import cloud_gen

app = Flask(__name__)
database_url = "mysql://starmap:starmapnyc@starmapdb.c4iz2nkqcg5a.us-east-1.rds.amazonaws.com/starmap"
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def home():
  return render_template('home.html')

@app.route('/', methods=['POST'])
def download_stl():
	output_style = request.form["output_style"]

	stars = cloud_gen.make_mock_stars()

	f = NamedTemporaryFile(delete=False)
	cloud_gen.render_scad(stars, f, output_style)
	f.close()
	return send_file(f.name, as_attachment=True, attachment_filename="starmap.scad", mimetype='application/octet-stream')

@app.route('/examples/hood/<n>')
def example_hood(n):
  if n == "random":
    n = random.randint(0,10)
  n = str(int(n))
  fn = "hood-" + n + ".scad"
  path = "/home/ec2-user/misc-data/examples/" + fn
  return send_file(path, as_attachment=True, attachment_filename=fn, mimetype='application/octet-stream')

if __name__ == "__main__":
    app.run(debug=True)
