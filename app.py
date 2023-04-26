from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'


# use the app.route() decorator to create a Flask view function called index()
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        choice = request.form['page_select']
        if choice == '':
            flash("A choice is required.")
        elif choice == "admin":
            return redirect(url_for('admin'))
        elif choice == "reservation":
            return redirect(url_for('reservations'))
    
    return render_template('index.html')

# use posts to show new infomration or put something specific on there, get is used to retreieve information

@app.route("/admin", methods=('GET', 'POST'))
def admin():
    return render_template('admin.html')

@app.route("/reservations", methods=('GET', 'POST'))
def reservations():
    return render_template('reservations.html')


app.run(host="0.0.0.0")