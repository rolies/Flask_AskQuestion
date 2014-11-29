import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'



# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
def connect_db(): 
    return sqlite3.connect(app.config['DATABASE'])

from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    return render_template('show_entries.html')

@app.route('/add', methods=['POST'])
def add_entry():
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('Your Question Alive')
    cur = g.db.execute('select id, title, text from entries order by id desc')
    entries = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]
    return render_template('show_post.html', entries=entries)

@app.route('/answer', methods=['GET', 'POST'])
def answer():


    g.db.commit()
    cur = g.db.execute('select id, title, text from entries order by id desc')
    entries = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]

    cur = g.db.execute('select answer, ident from answered')
    answered = [dict(answer=row[0], ident=row[1]) for row in cur.fetchall()]
    return render_template('all_post.html', answered=answered, entries=entries)

@app.route('/insert', methods=['POST'])
def insert_answer():
    g.db.execute('insert into answered (ident, answer) values (?, ?)',
                 [request.form['ident'], request.form['answered']])
    g.db.commit()
    cur = g.db.execute('select id, title, text from entries order by id desc')
    entries = [dict(id=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]

    cur = g.db.execute('select answer, ident from answered')
    answered = [dict(answer=row[0], ident=row[1]) for row in cur.fetchall()]
    return render_template('all_post.html', answered=answered, entries=entries)


if __name__ == '__main__':
    init_db()
    app.run()
