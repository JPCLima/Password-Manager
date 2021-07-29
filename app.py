from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__)
# Create sesssion & set permanet session to 5 min
app.secret_key = "key"
app.permanent_session_lifetime = timedelta(minutes=5)
# Config Database, Table records
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a Database
db = SQLAlchemy(app)

# Define a class to represent the records
class Records(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    application = db.Column("application", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, application, password):
        self.application = application   
        self.password = password   


@app.route('/')
def index():
    return render_template('results.html', all_records=Records.query.all())

@app.route('/new', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        application = request.form["application"]
        password = request.form["password"]
        rec = Records(application, password)

        # Save rec in the Database
        db.session.add(rec)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('new.html')

@app.route('/edit/<r>', methods=['POST', 'GET'])
def edit(r):
    # ID from the record
    record = Records.query.get(r) 
    if request.method == 'POST':
        # Get the date from the form 
        application = request.form["application"]
        password = request.form["password"]

        # Update the data
        record.application = application
        record.password = password
        
        # Save changes in the Database
        db.session.commit()

        return redirect(url_for('index'))
    else:              
        return render_template('edit.html', record=record)

   
@app.route('/search')
def search():
    word = request.args.get('search')
    print(f'---------------------------------------{word}')



    if word == '':     
        return render_template('search.html', records=Records.query.all())

    else:        
        return render_template('search.html', records=Records.query.filter(Records.application.startswith(word)).all())



    #search_query = Records.query.filter(Records.application.like(key))
    #return render_template('search.html', key=key, search_query=search_query)

if __name__ == '__main__':
    # Create a Database
    db.create_all()
    # Run the application
    app.run(debug=True)
