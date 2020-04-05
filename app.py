from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football_players.db'
db = SQLAlchemy(app)


class FootballPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(20), nullable=False, default='N/A')

    def __init__(self,name,age,nationality,positon):
        self.name = name
        self.age = age
        self.nationality = nationality
        self.position = positon

    def __repr__(self):
        return 'Football Player ' + str(self.id) + self.name


@app.route('/')
def Index():
    all_players = FootballPlayer.query.all()
    return render_template('index.html', players = all_players)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        nationality = request.form['nationality']
        position = request.form['position']

        my_player = FootballPlayer(name,age,nationality,position)
        db.session.add(my_player)
        db.session.commit()
        flash('Player inserted successfully')
    return redirect(url_for('Index'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_player = FootballPlayer.query.get(request.form.get('id'))

        my_player.name = request.form['name']
        my_player.age = request.form['age']
        my_player.nationality = request.form['nationality']
        my_player.position = request.form['position']

        db.session.commit()
        flash('Employee updated successfully')

        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def deleted(id):
    my_player = FootballPlayer.query.get(id)
    db.session.delete(my_player)
    db.session.commit()
    flash('Player deleted successfully')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
