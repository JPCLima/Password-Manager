from flask import Flask, render_template, request, redirect, url_for, session
import sqlalchemy

app = Flask(__name__)
app.secret_key = "key"

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/new', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        session['application'] = request.form.get('application')
        return redirect(url_for('application'))
    else:
        return render_template('new.html')

@app.route('/application')
def application():
    if "application" in session:
        application = session["application"]
        return f'<h1>{application}</h1>'
    else: 
        return redirect(url_from('index.html'))
    

if __name__ == '__main__':
    app.run(debug=True)
