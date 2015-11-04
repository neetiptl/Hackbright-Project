"""PROJECT."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, List, Group, To_Do, Shopping


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


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
    """login info"""

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
    """register"""

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

@app.route('/existing_lists')
def existing_lists():
    """show user's lists"""

    user_id = session["user_id"]
    user_list_groups = Group.query.filter_by(user_id=user_id).all()

    return render_template("existing_lists.html", user_list_groups=user_list_groups)

@app.route('/lists/<int:list_id>')
def lists(list_id):
    """get items in user's list"""

    this_list = List.query.filter_by(list_id=list_id).one()
    print "\n\n\n\n\n\n"
    print this_list

    return render_template("list_items.html", this_list=this_list)

@app.route('/new_list', methods=["POST"])
def new_list():



    return render_template("new_list.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
