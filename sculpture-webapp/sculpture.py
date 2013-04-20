import os
from flask import Flask
from flask import render_template
from flask import Response
from flask import send_file
from tempfile import NamedTemporaryFile

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
  return render_template('home.html')

@app.route('/', methods=['POST'])
def download_stl():
  f = NamedTemporaryFile(delete=False)
  f.write("STARMAP")
  f.close()
  return send_file(f.name, as_attachment=True, attachment_filename="starmap.stl", mimetype='application/octet-stream')

if __name__ == "__main__":
    app.run(debug=True)
