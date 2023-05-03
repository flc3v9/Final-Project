from flask import Flask, render_template, request, url_for, flash, redirect, abort
import reservations as seats

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

# use the app.route() decorator to create a Flask view function called index()
# use posts to show new infomration or put something specific on there, get is used to retreieve information
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

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def determine_sales(chart):

    # get cost matrix
    cost_matrix = get_cost_matrix()
    # create sales variable
    total_sales = 0
    # add to sales for each reserved seat
    for row in range(len(chart)):
        for seat in range(len(chart[row])):
            if chart[row][seat] == 'X':
                total_sales += cost_matrix[row][seat]
    # create sale string
    string_sales = "$" + str(total_sales)
    # return final string
    return string_sales

#admin login 
def admin_login(login_user, login_pass):
    #opens file
    file_open = open("passcodes.txt","r")

    #list to append set login info
    user_list=[]
    #appends login info from textfile
    for line in file_open.readlines():
        line = line.strip()
        user, password = line.split(', ')
        user_list.append((user, password))
        
    while True:
        verify = False
        #Checks user, password against sets of tuples in user_list
        for user, password in user_list:
            if login_user == user and login_pass == password:
                verify = True
                file_open.close()
                return verify

        return verify

@app.route("/admin", methods=('GET', 'POST'))
def admin():
    if request.method == "GET":
        return render_template('admin.html')

    if request.method == "POST":
        # get form input
        username = request.form['username']
        password = request.form['password']

        # user authentication
        is_admin = admin_login(username, password)

        if username == '':
            flash("A username is required.")
            return render_template('admin.html')
        elif password == '':
            flash("A password is required.")
            return render_template('admin.html')
        elif is_admin == False:
            flash("Invalid username/password combination.")
            return render_template('admin.html')
        
        # get current seat chart
        seat_chart = seats.get_seat_chart()
        # get current sales
        sales = determine_sales(seat_chart)

        # render page with seat chart and sales
        return render_template('admin.html', sales=sales, seat_chart=seat_chart)

@app.route("/reservations", methods=('GET', 'POST'))
def reservations():
    if request.method == "GET":
        # try to render seat chart, but if it fails render page without it 
        try:
            seat_chart = seats.get_seat_chart()
            return render_template('reservations.html', seat_chart=seat_chart)
        except:
            flash("Sorry, something went wrong with loading the seating chart. Please try again later.")
            return render_template('reservations.html')
    
    if request.method == "POST":
        # try to render seat chart, but if it fails render page without it 
        try:
            # get current seat chart
            seat_chart = seats.get_seat_chart()
            # try to get input, make reservation, and print success message
            try:
                # get form data
                first_name = request.form["first_name"]
                if first_name == "":
                    flash("You must enter a first name.")
                    return render_template('reservations.html', seat_chart=seat_chart)
                last_name = request.form["last_name"]
                if last_name == "":
                    flash("You must enter a last name.")
                    return render_template('reservations.html', seat_chart=seat_chart)
                row = request.form["row"]
                if row == "":
                    flash("You must select a row.")
                    return render_template('reservations.html', seat_chart=seat_chart)
                seat = request.form["seat"]
                if seat == "":
                    flash("You must select a seat.")
                    return render_template('reservations.html', seat_chart=seat_chart)
                
                # check if reservation already exists
                if seat_chart[int(row)][int(seat)] == "X":
                    flash("Sorry, that seat is already reserved.")
                    return render_template('reservations.html', seat_chart=seat_chart)

                # create ticket number
                ticketNumber = seats.get_ticket(first_name)

                # update reservations.txt
                with open('reservations.txt', 'a') as seat_file:
                    entry = f"{first_name}, {row}, {seat}, {ticketNumber}\n"
                    seat_file.write(entry)
                
                # get new seat chart
                seat_chart = seats.get_seat_chart()
                # success message
                success_message = f"Congratulations {first_name}! Row: {int(row)+1} Seat: {int(seat)+1} is now reserved for you. Enjoy your trip!<br>Your eTicket number is: {ticketNumber}"
                return render_template('reservations.html', seat_chart=seat_chart, success_message=success_message)
            except:
                flash("Sorry, something went wrong. Please try again.")
                return render_template('reservations.html', seat_chart=seat_chart)
        except:
            flash("Sorry, something went wrong with loading the seating chart. Please try again later.")
            return render_template('reservations.html')

app.run(host="0.0.0.0")