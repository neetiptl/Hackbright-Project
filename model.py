"""Models and database functions for Project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Nucleus/Family Network/Shared list."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name=db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    user_location_name = db.Column(db.String, nullable = True)
    user_location_address = db.Column(db.String(100), nullable = True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "User ID: {}, Name: {}, email:{}, password: {}, mobile#: {}, \
                User location: {}, User Address: {}".format(self.user_id,
                                                                self.name, 
                                                                self.email, 
                                                                self.password, 
                                                                self.mobile,
                                                                self.user_location_name, 
                                                                self.user_location_address)


class List(db.Model):
    """The list."""

    __tablename__ = "lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    list_type = db.Column(db.String(20))
    due_date_list = db.Column(db.DateTime, nullable=True)
    list_location_name = db.Column(db.String(50), nullable=True)
    list_location_address = db.Column(db.String(100), nullable=True)
    created_by = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "List ID: {}, List name: {}, List Type:{}, due_date: {}, \
                list location: {}, list Address: {}, Created by: {}".format(self.list_id,
                                                                            self.name, 
                                                                            self.list_type, 
                                                                            self.due_date_list,
                                                                            self.list_location_name,
                                                                            self.list_location_address, 
                                                                            self.created_by)
class Group(db.Model):
    """Tying users and lists"""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    list_id = db.Column(db.Integer,db.ForeignKey('lists.list_id'))
    permission = db.Column(db.Boolean, nullable = False, default = True)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("groups"))

    # Define relationship to list
    checklist = db.relationship("List",
                            backref=db.backref("groups"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "Group ID: {}, User ID: {}, List ID: {}".format(self.group_id,
                                                                self.user_id, 
                                                                self.list_id,
                                                                self.permission)




class To_Do(db.Model):
    """To-Do list list type"""

    __tablename__ = "to_dos"

    to_do_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    item = db.Column(db.String(64), nullable=False)
    due_date_todo = db.Column(db.DateTime, nullable=True)
    status_notdone = db.Column(db.Boolean, nullable=False, default=True)
    todo_location_name = db.Column(db.String(100), nullable=True)
    todo_location_address = db.Column(db.String(100), nullable=True)

    #Define relationship to lists
    list_todo = db.relationship("List",
                                backref=db.backref("to_dos"))
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "List_Items ID:{}, List ID: {}, Item: {}, Due Date: {}, \
                Status(ongoing?): {}".format(self.to_do_id,
                                            self.list_id, 
                                            self.item, 
                                            self.due_date_todo,
                                            self.status_notdone,
                                            self.todo_location_name,
                                            self.todo_location_address)



class Shopping(db.Model):
    """Shopping list list type"""

    __tablename__ = "shoppings"

    shopping_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    item = db.Column(db.String(64), nullable=True)
    due_date_shopping = db.Column(db.DateTime, nullable=True)
    status_notdone = db.Column(db.Boolean, nullable=False, default=True)

    #Define relationship to lists
    list_shopping = db.relationship("List",
                                backref=db.backref("shoppings"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "List_Items ID:{}, List ID: {}, Item: {}, \
                Due Date: {}, Status(ongoing?): {}".format(self.shopping_id,
                                                            self.list_id, 
                                                            self.item, 
                                                            self.due_date_shopping, 
                                                            self.status_notdone)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # if we run this module interactively, able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
