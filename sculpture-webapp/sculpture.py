import os
from flask import Flask, Response, render_template, send_file, request
from flask.ext.sqlalchemy import SQLAlchemy
from tempfile import NamedTemporaryFile

from lib import cloud_gen

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
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

if __name__ == "__main__":
    app.run(debug=True)
