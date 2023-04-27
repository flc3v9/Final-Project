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


'''
Function to generate cost matrix for flights
Input: none
Output: Returns a 12 x 4 matrix of prices
'''
def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def determine_sales():

    # delele this later once you input the branch as a function parameter
    chart = [['0', '0', 'X', '0'], ['0', 'X', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['X', '0', '0', '0'], ['0', '0', 'X', '0']]

    cost_matrix = get_cost_matrix()
    total_sales = 0

    for row in range(len(chart)):
        for seat in range(len(chart[row])):
            if chart[row][seat] == 'X':
                total_sales += cost_matrix[row][seat]

    string_sales = "$" + str(total_sales)
    # this can be returned later.
    return string_sales

@app.route("/admin", methods=('GET', 'POST'))
def admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == '':
            flash("A username is required.")
        elif password == '':
            flash("A password is required.")

    sales = determine_sales()
    return render_template('admin.html', sales=sales)

@app.route("/reservations", methods=('GET', 'POST'))
def reservations():
    return render_template('reservations.html')


app.run(host="0.0.0.0")