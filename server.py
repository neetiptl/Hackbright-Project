"""PROJECT."""

from jinja2 import StrictUndefined
import datetime
from flask import Flask, render_template, redirect, request, session, flash, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, List, Group, To_Do, Shopping
import json
import twilio.twiml
from twilio.rest import TwilioRestClient
import os
from geopy.geocoders import Nominatim
from geopy.distance import vincenty

sid = os.environ.get('TWILIO_ACCOUNT_SID')
token = os.environ.get('TWILIO_AUTH_TOKEN')
number = os.environ.get('TWILIO_NUMBER')
client = TwilioRestClient(sid, token)

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

################ Login, Logout, Account info and Registration routes #################
@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/login', methods=['GET'])
def login():
    """login"""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_info():
    """collect and check login info"""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found!")
        return redirect("/login")

    if user.password != password:
        flash("Wrong password")
        return redirect("/login")

    session["user_id"] = user.user_id
    session["user_name"] = user.name

    flash("Logged in")
    return redirect("/existing_lists")

@app.route('/register', methods=['GET'])
def register():
    """new user registration form"""

    return render_template("registration_form.html")

@app.route('/register', methods=['POST'])
def register_info():
    """Process registration"""

    # Get form variables
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    mobile = request.form["mobile"]
    user_location_name = request.form["location"]
    user_location_address = request.form["address"]

    new_user = User(name=name, email=email,
                    password=password,
                    mobile=mobile,
                    user_location_name=user_location_name,
                    user_location_address=user_location_address)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} added.".format(name))
    return redirect("/")

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route('/account_info')
def account_info():
    """Display account information"""
    
    user_info = User.query.filter_by(user_id=session["user_id"]).one()

    return render_template("account_info.html", user_info=user_info)


#################SHOW ABOUT PAGE#################################


@app.route('/about')
def show_about_page():
    """Display About page."""

    return render_template('about.html')



################ Display existing lists route ##############
@app.route('/existing_lists')
def existing_lists():
    """show user's lists"""

    user_id = session["user_id"]
    user_list_groups = Group.query.filter_by(user_id=user_id).all()

    return render_template("existing_lists.html", user_list_groups=user_list_groups)

@app.route('/lists/<int:list_id>')
def lists(list_id):
    """get user's list"""

    this_list = List.query.filter_by(list_id=list_id).one()
    permissions = Group.query.filter_by(list_id=list_id).all()
    # print permissions
    list_type = this_list.list_type
    # print list_type


    return render_template("list_items.html", this_list=this_list, 
                                            permissions=permissions, 
                                            list_type=list_type)



############### Create new lists routes  ###################
@app.route('/new_list_base', methods=["GET"])
def new_list_base():

    return render_template("new_list_base.html")


@app.route('/new_list_base', methods=['POST'])
def base_form():

#Get form data and add to database
    name = request.form['name']
    due_date_list = request.form['due-date-list']
    list_location_name = request.form['list_location_name']
    list_location_address = request.form['list_location_address']
    list_type = request.form['list-type']
    created_by = session["user_id"]
    due_date_list = datetime.datetime.strptime(due_date_list, "%m/%d/%Y")
    created_by_name_obj = User.query.filter_by(user_id=created_by).one()
    created_by_name = created_by_name_obj.name
#FIXME - change created_by to int, then commit created_by=created_by
#add to list table
    list_ = List(name=name,
                list_type=list_type, 
                due_date_list=due_date_list, 
                list_location_address=list_location_address,
                list_location_name=list_location_name,
                created_by=created_by_name)
    # print "list: ", list_
    db.session.add(list_)
    db.session.commit()
#add user to groups table
    groups = Group(user_id=created_by,
                    list_id=list_.list_id,
                    permission = True)
    db.session.add(groups)
    db.session.commit()
    # print "group: ", groups

#add new users to groups table
#FIXME: add more users
#FIXME: add users where only have read permission, not write (e.g. permssion = False)
    user_name_permissions = request.form.get('listPermissions')
    print "user_name_permissions", user_name_permissions
    if user_name_permissions:
        user_being_added = User.query.filter_by(name=user_name_permissions).one()
        user_being_added_mobile = user_being_added.mobile
        # print "user_being_added", user_being_added
        user_permissions_row = Group(user_id=user_being_added.user_id,
                                    list_id=list_.list_id,
                                    permission = True)
        # print "user_permissions_row", user_permissions_row
        print user_permissions_row.group_id

        # ask person being added if they want to be added to the list
        message = "{}, {} is trying to add you to {} (list id = {}. Reply yes followed by the list id if you want to be added.".format(user_being_added.name, created_by_name, name, list_.list_id)
        client.messages.create(to = user_being_added_mobile, 
                                    from_="+17329926464", 
                                    body=message)

    return redirect(url_for('lists', list_id=list_.list_id))

@app.route('/inbound', methods=['POST'])
def get_twilio_response():
    """ Save to db if incoming text is 'Yes' """
    resp = twilio.twiml.Response()
    body = request.form['Body']
    message, list_id = body.split(' ')
    print message, list_id
    resp.sms("Hello, Mobile Monkey")
    from_number = request.values.get('From', None)
    from_number = from_number.lstrip('+1')
    print "from_number", from_number
    if message == 'Yes':
        user_permissions_row = User.query.filter_by(mobile=from_number).first() #should be .one() but all the numbers in the database are my cell #
        groups = Group(user_id=user_permissions_row.user_id,
                    list_id=list_id,
                    permission = True)
        db.session.add(groups)
        db.session.commit()
        print groups
    return str(resp)


@app.route('/new_todo/<int:list_id>', methods=['POST'])
def new_todo(list_id):
    """collect new todo list form"""

    item_list = request.form.get('item')
    due_date_todo_list = request.form.get('due_date_todo')
    status_notdone_list = request.form.get('status_notdone')
    todo_location_name_list = request.form.get('todo_location_name')
    todo_location_address = request.form.get('todo_location_address')
    todo_location_address_list = request.form.get('todo_location_address')

    item = item_list
    due_date_todo = due_date_todo_list
    if status_notdone_list=='on':
        status_notdone = False
    else:
        status_notdone = True
    todo_location_name = todo_location_name_list
    todo_location_address = todo_location_address_list
    if due_date_todo:
        due_date_todo = datetime.datetime.strptime(due_date_todo, "%m/%d/%Y")
    else:
        due_date_todo = None

    new_todo = To_Do(list_id=list_id,
                    item=item,
                    due_date_todo=due_date_todo,
                    status_notdone=status_notdone,
                    todo_location_name=todo_location_name,
                    todo_location_address=todo_location_address)

    db.session.add(new_todo)
    db.session.commit()
    # print "\n\n\n\n New ToDo:"
    # print new_todo
    # print "new todo json_list", json_list(list_id)
    return json_list(list_id)

@app.route("/new_shopping/<int:list_id>", methods=["POST"])
def new_shopping(list_id):
    """get shopping form data and commit it"""

    item_list = request.form.get('item')
    status_notdone_list = request.form.get('status_notdone')

    item = item_list
    if status_notdone_list=='on':
        status_notdone = False
    else:
        status_notdone = True

    new_shopping = Shopping(list_id=list_id,
                    item=item,
                    status_notdone=status_notdone)

    db.session.add(new_shopping)
    db.session.commit()
    # print "\n\n\n\n New Shopping item:"
    # print new_shopping
    # print "new shopping json_list", json_list(list_id)

    return json_list(list_id)

@app.route("/change_task_status", methods=["POST"])
def change_task_status():
    """Change list status if task is complete"""
    list_types = request.form.get('listtype')
    list_type_id = request.form.get('idOfClickedButton')
    # print "\n\n\n\n", "in change task status route", list_types, list_type_id

    ## Update row in shoppings or to_dos table)
    if  list_types == "ToDo":
        list_row = To_Do.query.filter_by(to_do_id=list_type_id).one()
        list_row.status_notdone = False
        # print list_row
        list_id = list_row.list_id
    elif list_types == "Shopping":
        list_row = Shopping.query.filter_by(shopping_id=list_type_id).one()
        list_row.status_notdone = False
        # print list_row
        list_id = list_row.list_id

    db.session.commit()



    return json_list(list_id)


def json_list(list_id):
    """Given a list ID, return json string of list"""

    this_list = List.query.filter_by(list_id=list_id).one()
    current_list_json = []
    # print this_list

    if this_list.list_type == 'shopping':
        for item in this_list.shoppings:
            # print "item", item
            current_list_json.append({ "shopping_id": item.shopping_id,
                                        "list_id" : item.list_id,
                                        "item" : item.item,
                                        "status_notdone" : item.status_notdone
                                      })

    if this_list.list_type == 'to-do':
        for item in this_list.to_dos:
            # print "item", item
            print "\n\n\n item due_date_todo", item.due_date_todo
            if item.due_date_todo:
                due_date_todo = item.due_date_todo.strftime("%Y-%m-%d")
            else:
                due_date_todo = "None"
            print due_date_todo
            current_list_json.append({ "to_do_id": item.to_do_id,
                                        "list_id" : item.list_id,
                                        "item" : item.item,
                                        "due_date_todo" : due_date_todo,
                                        "status_notdone" : item.status_notdone,
                                        "todo_location_name" : item.todo_location_name,
                                        "todo_location_address" : item.todo_location_address
                                    })
    # print current_list_json

    # Twilio notification to all users on list
    twilio_texts_list_edits(list_id)


    # return json to ajax
    current_list_json_string = json.dumps(current_list_json)
    return current_list_json_string



#######TWILIO#############
def twilio_texts_list_edits(list_id):
    """Respond to db changes with a text message to ppl on list."""

    users_on_this_list = Group.query.filter_by(list_id=list_id).all()
    current_list = List.query.filter_by(list_id=list_id).one()
    current_user = session["user_id"]
    current_user_name = User.query.filter_by(user_id=current_user).one()
    current_user_name = current_user_name.name
    list_name = current_list.name

    for person in users_on_this_list:
        if person.user_id != current_user:
            mobile_number = person.user.mobile
            other_persons_name = person.user.name
            print mobile_number
            message = "Hi {}! FYI, {} edited {}".format(other_persons_name, current_user_name,list_name)
            print "message", message

            client.messages.create(to = mobile_number, 
                                from_="+17329926464", 
                                body=message)
    return 


#########LOCATION############
@app.route("/location", methods = ["GET"])
def location():
    """If user's browser/login location is close to locations of his/her list, send a Twilio text."""

#latitude and longitude(from browser) of the currently logged-in user
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    # print "\n\n\n\n position from browser", lat, lon
    current_location = (lat, lon)

#lists current user is included on
    current_user = session["user_id"]
    current_user_lists = Group.query.filter_by(user_id=current_user).all()

    current_user_obj = User.query.filter_by(user_id=current_user).one()
    mobile_number = current_user_obj.mobile
    print mobile_number

#Loop through current user's lists and find distance between the list and the user.
# If they're very close, remind the user to take care of the list.
    for list_ in current_user_lists:
        if (list_.checklist.list_location_address):
            address = list_.checklist.list_location_address
            # print "address", address
#Nominatim:tool to search OSM by address and to generate synthetic addresses of OSM points (reverse geocoding). 
            geolocator = Nominatim()
            try:
                location = geolocator.geocode(address)
            except:
                location = None
            print location

            if location != None:
                print(location.address)
                list_location = ((location.latitude, location.longitude))
                distance = (vincenty(current_location, list_location).miles)
                if distance <= 2:
                    message = "{} is less than 2 miles from your location. Maybe you should take care of {}.".format(location.address, list_.checklist.name)
                    client.messages.create(to = mobile_number, 
                                from_="+17329926464", 
                                body=message)

    return "success"

@app.route("/show_location", methods=["GET"])
def get_location():
    """get location for map"""

    return "success"
################ Debug Toolbar #########################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
