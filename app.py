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
    if request.method == 'POST':
        first_name = request.form['first_name']
        row = request.form['row']
        seat = request.form['seat']
        ticket_str = ticket(first_name)  # call the ticket function after first_name is assigned
        # Save the data to file
        with open('reservations.txt', 'a') as file:
            file.write(f'{first_name}, {row}, {seat}, {ticket_str}\n')
        return render_template('success.html', name=first_name, ticket=ticket_str)
    return render_template('reservations.html')

def ticket(first_name):
    class_name = "INFOTC4320"
    nameLength = int(len(first_name))
    class_nameLength = int(len(class_name))
    nameRange = nameLength + class_nameLength
    list1 = []
    count = 0
    for name_char in range(0,nameRange-1):
        list1.append(first_name[count])
        list1.append(class_name[count])
        count+=1
        if (count == nameLength-1):
            break
    ticket= ''.join(list1)+'4320'
    return ticket



app.run(host="0.0.0.0")