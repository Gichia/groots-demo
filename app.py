import sqlite3
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = "peter"

@app.route('/home')
def home():
  return render_template('base.html')

@app.route('/assets')
def assets():
  query = """
    SELECT e.id, e.name, e.description, e.cost, e.quantity, c.name AS category
    FROM equipments AS e 
    JOIN categories AS c 
    ON e.category_id = c.id
    ORDER BY e.id DESC
  """
  query1 = "SELECT * FROM categories"

  connection = sqlite3.connect('data.db')
  cursor = connection.cursor()

  cursor.execute(query)
  equipment = cursor.fetchall()
  cursor.execute(query1)
  categories = cursor.fetchall()
  connection.close()
  return render_template('assets.html', equipment=equipment, categories=categories)

@app.route('/add', methods=['POST'])
def add_equipment():
  user_data = request.get_json()
  if user_data:
    name = user_data['name']
    description = user_data['description']
    category_id = user_data['category']
    cost = user_data['cost']
    quantity = user_data['quantity']

    query = "INSERT INTO equipments (name, description, category_id, cost, quantity) VALUES(?, ?, ?, ?, ?)"

    try:
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()
      cursor.execute(query, (name, description, category_id, cost, quantity))
      connection.commit()
      connection.close()
      return {'message': 'Successfully saved!'}, 201
    except Exception as err:
      return {'error': f"An error '{err}' occured!"}, 500

@app.route('/meetings', methods=['GET', 'POST'])
def meetings():
  if request.method == 'GET':
    query = """
      SELECT m.topic, m.location, m.date_held, g.name,
        (SELECT SUM(b.group_id) FROM members AS b WHERE b.group_id = m.group_id GROUP BY b.group_id)
      FROM meetings AS m
      JOIN groups AS g ON m.group_id = g.id
      ORDER BY m.id ASC
    """
    query1 = "SELECT * FROM groups"

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(query)
    meetings = cursor.fetchall()
    cursor.execute(query1)
    groups = cursor.fetchall()
    connection.close()
    return render_template('meetings.html', meetings=meetings, groups=groups)
  elif request.method == 'POST':
    meeting_data = request.get_json()
    query = "INSERT INTO meetings (group_id, topic, location, date_held) VALUES(?,?,?,?)"

    try:
      group_id = meeting_data['groupId']
      topic = meeting_data['topic']
      location = meeting_data['location']
      date_held = meeting_data['dateHeld']

      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()
      cursor.execute(query, (group_id, topic, location, date_held))
      connection.commit()
      connection.close()
      return {'message': 'Success'}, 200
    except:
      return {'error': 'An error occured!'}, 500


@app.route('/members', methods=['GET', 'POST'])
def members():
  if request.method == 'GET':
    query = """
      SELECT m.id, m.first_name, m.last_name, m.gender, m.age, g.name
      FROM members AS m
      JOIN groups AS g
      ON m.group_id = g.id
      ORDER BY m.id DESC
    """
    query1 = "SELECT * FROM groups"

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(query)
    members = cursor.fetchall()
    cursor.execute(query1)
    groups = cursor.fetchall()
    connection.close()
    return render_template('members.html', members=members, groups=groups)
  elif request.method == 'POST':
    data = request.get_json()
    query = "INSERT INTO members (first_name, last_name, group_id, gender, age) VALUES (?,?,?,?,?)"

    try:
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()
      cursor.execute(query, (data['fname'], data['lname'], data['group_id'], data['gender'], data['age']))
      connection.commit()
      connection.close()
      return {'message': 'Successfully saved!'}, 201
    except Exception as err:
      return {'error': f"An error '{err}' occured!"}, 500

@app.route('/')
@app.route('/auth/login', methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    user_data = request.form

    if user_data['email'] == 'chrisn@gmail.com' and user_data['password'] == '12345':
      flash('You have been successfully logged in!', 'success')
      return redirect(url_for('home'))

    flash('Incorrect details', 'warning')
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
  flash('You have been logged out!', 'warning')
  return render_template('logout.html')


if __name__ == '__main__':
  app.run(debug=True)
