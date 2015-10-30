"""PROJECT."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


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
    return redirect('/')

@app.route('/register', methods=['GET'])
def register():
    """register"""

    return render_template("register.html")

@app.route('/register', methods=['GET'])
def register_info():
    """register"""

    return render_template("register.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
