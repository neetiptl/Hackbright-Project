"""PROJECT."""

from jinja2 import StrictUndefined
import datetime
from flask import Flask, render_template, redirect, request, session, flash, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, List, Group, To_Do, Shopping
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

################ Login, Logout, and Registration routes #################
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

    flash("Logged in")
 #   return redirect("/users/%s" % user.user_id)
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
    print permissions
    list_type = this_list.list_type
    print list_type


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
    list_ = List(name=name,
                list_type=list_type, 
                due_date_list=due_date_list, 
                list_location_address=list_location_address,
                list_location_name=list_location_name,
                created_by=created_by_name)
    print "list: ", list_
    db.session.add(list_)
    db.session.commit()

    groups = Group(user_id=created_by,
                    list_id=list_.list_id,
                    permission = True)
    db.session.add(groups)
    db.session.commit()
    print "group: ", groups

    #add new users to list
    user_name_permissions = request.form.get('listPermissions')
    print "user_name_permissions", user_name_permissions
    user_being_added = User.query.filter_by(name=user_name_permissions).one()
    print "user_being_added", user_being_added
    user_permissions_row = Group(user_id=user_being_added.user_id,
                                list_id=list_.list_id,
                                permission = True)
    print "user_permissions_row", user_permissions_row
    db.session.add(groups)
    db.session.commit()

    return redirect(url_for('lists', list_id=list_.list_id))

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
    print "\n\n\n\n New ToDo:"
    print new_todo
    print "new todo json_list", json_list(list_id)
    return json_list(list_id)
    # todo_dict = {
    #     "to_do_id" : new_todo.to_do_id,
    #     "list_id" : new_todo.list_id,
    #     "item" : new_todo.item,
    #     "due_date_todo" : new_todo.due_date_todo,
    #     "status_notdone" : new_todo.status_notdone,
    #     "todo_location_name" : new_todo.todo_location_name,
    #     "todo_location_address" : new_todo.todo_location_address
    # }
    # return jsonify(todo_dict)

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
    print "\n\n\n\n New Shopping item:"
    print new_shopping
    print "new shopping json_list", json_list(list_id)
    return json_list(list_id)
    # shopping_dict = {
    #     "list_id" : new_shopping.list_id,
    #     "item" : new_shopping.item,
    #     "status_notdone" : new_shopping.status_notdone
    # }

    # return jsonify(shopping_dict)

@app.route("/change_task_status", methods=["POST"])
def change_task_status():
    """Change list status if task is complete"""
    list_types = request.form.get('listtype')
    list_type_id = request.form.get('idOfClickedButton')
    print "\n\n\n\n", "in change task status route", list_types, list_type_id

    ## Update row in shoppings or to_dos table)
    if  list_types == "ToDo":
        list_row = To_Do.query.filter_by(to_do_id=list_type_id).one()
        list_row.status_notdone = False
        print list_row
        list_id = list_row.list_id
    elif list_types == "Shopping":
        list_row = Shopping.query.filter_by(shopping_id=list_type_id).one()
        list_row.status_notdone = False
        print list_row
        list_id = list_row.list_id

    db.session.commit()
    return json_list(list_id)


def json_list(list_id):
    """Given a list ID, return json string of list"""

    this_list = List.query.filter_by(list_id=list_id).one()
    current_list_json = []
    print this_list

    if this_list.list_type == 'shopping':
        for item in this_list.shoppings:
            print "item", item
            current_list_json.append = ({ "shopping_id": item.shopping_id,
                                        "list_id" : item.list_id,
                                        "item" : item.item,
                                        "status_notdone" : item.status_notdone
                                      })

    if this_list.list_type == 'to-do':
        for item in this_list.to_dos:
            print "item", item
            current_list_json.append({ "to_do_id": item.to_do_id,
                                        "list_id" : item.list_id,
                                        "item" : item.item,
                                        "due_date_todo" : item.due_date_todo.strftime("%Y-%m-%d"),
                                        "status_notdone" : item.status_notdone,
                                        "todo_location_name" : item.todo_location_name,
                                        "todo_location_address" : item.todo_location_address
                                    })
    print current_list_json

    # return json to ajax
    current_list_json_string = json.dumps(current_list_json)
    return current_list_json_string

################ Debug Toolbar #########################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
