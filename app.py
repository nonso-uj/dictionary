from flask import Flask, render_template, url_for, request, flash, current_app
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import os

app = Flask(__name__)

app.secret_key = 'secret'
app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_DB'] ='dictionary'
app.config['MYSQL_DATABASE_USER'] ='user'
app.config['MYSQL_DATABASE_PASSWORD'] ='root'

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def home():
  user_response = ''

  if request.method == 'POST':
    user_input = request.form['word']
    if user_input == '':
      flash('You did not enter a valid word, please try again.', 'flash_error')
    else:
      conn = mysql.get_db()
      cur= conn.cursor()
      cur.execute('select meaning from word where word = %s', (user_input))
      rv = cur.fetchall()
      if (len(rv) > 0):
        user_response = rv[0]['meaning']
      else:
        flash("Word not found in the dictionary, please try another", 'flash_error')

  return render_template('home.html', user_response = user_response)




@app.route('/dashboard')
def dashboard():
  conn = mysql.get_db()
  cur = conn.cursor()
  cur.execute('select * from word')
  rv = cur.fetchall()

  return render_template('dashboard.html', words = rv)


@app.route('/word', methods = ['POST'])
def add_word():
  req = request.get_json()
  word = req['word']
  meaning = req['meaning']
  if word =='' or meaning == '':
    flash('Please fill in the required fields!!', 'flash_error')
  else:
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('insert into word(word, meaning) VALUES (%s, %s)', (word, meaning))
    conn.commit()
    cur.close()
    flash('Word successfully added!!', 'flash_success')

  return json.dumps('success')



@app.route('/word/<id>/delete', methods = ['POST'])
def delete_word(id):
  word_id = id
  conn = mysql.get_db()
  cur = conn.cursor()
  cur.execute('delete from word where id = %s', (word_id))
  conn.commit()
  cur.close()
  flash('Word successfully deleted!!', 'flash_success')

  return json.dumps('success')


@app.route('/word/<id>/edit', methods=['POST'])
def edit_word(id):
  word_id = id
  req = request.get_json()
  word = req['word']
  meaning = req['meaning']
  if word =='' or meaning == '':
    flash('Please fill in the required fields!!', 'flash_error')
  else:
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('update word set word=%s, meaning=%s where id=%s', (word, meaning, word_id))
    conn.commit()
    cur.close()
    flash('Word successfully edited!!', 'flash_success')

  return json.dumps('success')



@app.route('/add_logo', methods=['POST'])
def add_logo():
  image = request.files['file']

  if image:
    filepath = os.path.join(current_app.root_path, 'static/images/logo.png')
    image.save(filepath)
    flash('Image successfully uploaded!', 'flash_success')
  else:
    flash('There was an Error!', 'flash_error')

  return 'Success'



if __name__ == "__main__":
  app.run(debug = True)