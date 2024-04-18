from flask import Flask, render_template, request, redirect, flash, url_for, g
import main
import urllib.request
from app import app
import sqlite3 as sql
from werkzeug.utils import secure_filename
from main import getPrediction
import os

fishdb = 'goldfishdb.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(fishdb)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pred')
def pred():
    return render_template('prediction.html')

@app.route('/prediction', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("static/uploads/",filename))
            getPrediction(filename)
            label, acc = getPrediction(filename)
            return redirect('/goldfish/'+label)

@app.route('/gfdb')
def gflist():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM goldfishtable')
    articles = cur.fetchall()
    return render_template('gfdb.html', articles=articles)

@app.route('/goldfish/<int:goldfish_id>')
def fishinfo(goldfish_id):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM goldfishtable WHERE goldfishid = ?', (goldfish_id,))
    info = cur.fetchone()
    return render_template('gfinfo.html', post=info)


@app.route('/about')
def about():
    return render_template('about.html')




if __name__ == "__main__":
    app.run()