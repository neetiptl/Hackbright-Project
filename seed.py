import datetime

from model import User, List, Group, To_Do, Shopping, connect_to_db, db
from server import app


def load_users():

    print "Users"
    for i, row in enumerate(open("data/users")):
        row = row.rstrip()
        name, mobile, email, password, user_location_name, user_location_address = row.split("|")

        user = User(name=name,
                    email=email,
                    password=password,
                    mobile=mobile,
                    user_location_name=user_location_name,
                    user_location_address=user_location_address
                    )

        # Add to session
        db.session.add(user)

    # Commit work
    db.session.commit()


def load_lists():

    print "Lists"
    for i, row in enumerate(open("data/lists")):
        row = row.rstrip()
        name, list_type, due_date_list, list_location_name, list_location_address, created_by= row.split("|")

        # The date is in the file as month-day-year
        # convert it to a datetime object.

        if due_date_list:
            due_date_list = datetime.datetime.strptime(due_date_list, "%m-%d-%y")
        else:
            due_date_list = None

        listt = List(name=name,
                    list_type=list_type,
                    due_date_list=due_date_list,
                    list_location_name=list_location_name,
                    list_location_address=list_location_address,
                    created_by=created_by
                    )

        # Add to session
        db.session.add(listt)

    # Commit work
    db.session.commit()

def load_groups():

    print "Groups"
    for i, row in enumerate(open("data/groups")):
        row = row.rstrip()
        user_id, list_id, permission= row.split("|")

        group = Group(user_id=user_id,
                    list_id=list_id,
                    permission=permission
                   )

        # Add to session
        db.session.add(group)

    # Commit work
    db.session.commit()

def load_todo():

    print "To_Do"
    for i, row in enumerate(open("data/todo")):
        row = row.rstrip()
        list_id, item, due_date_todo, status_notdone, todo_location_name, todo_location_address= row.split("|")

        # The date is in the file as month-day-year
        # convert it to a datetime object.

        if due_date_todo:
            due_date_todo = datetime.datetime.strptime(due_date_todo, "%m-%d-%y")
        else:
            due_date_todo = None

        todo = To_Do(list_id=list_id,
                    item=item,
                    due_date_todo=due_date_todo,
                    status_notdone=status_notdone,
                    todo_location_name=todo_location_name,
                    todo_location_address=todo_location_address
                    )

        # Add to session
        db.session.add(todo)

    # Commit work
    db.session.commit()

def load_shopping():

    print "Shopping"
    for i, row in enumerate(open("data/shopping")):
        row = row.rstrip()
        list_id, item, due_date_shopping, status_notdone= row.split("|")

        # The date is in the file as month-day-year
        # convert it to a datetime object.

        if due_date_shopping:
            due_date_shopping = datetime.datetime.strptime(due_date_shopping, "%m-%d-%y")
        else:
            due_date_shopping = None

        shoppings = Shopping(list_id=list_id,
                        item=item,
                        due_date_shopping=due_date_shopping,
                        status_notdone=status_notdone,
                    )

        # Add to session
        db.session.add(shoppings)

    # Commit work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_shopping()
    load_todo()
    load_groups()
    load_lists()
