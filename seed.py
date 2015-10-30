import datetime

from model import User, List, Group, To_Do, Shopping
from server import app


def load_users():

    print "Users"
    for i, row in enumerate(open("data/users")):
        row = row.rstrip()
        user_id, name, email, password, mobile, user_location_name, user_location_address = row.split("|")

        user = User(user_id=user_id,
                    name=name,
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
        list_id, name, list_type, due_date, list_location_name, list_location_address= row.split("|")

        user = User(list_id=list_id,
                    name=name,
                    list_type=list_type,
                    due_date=due_date,
                    list_location_name=list_location_name,
                    list_location_address=list_location_address
                    )

        # Add to session
        db.session.add(user)

    # Commit work
    db.session.commit()

def load_groups():

    print "Groups"
    for i, row in enumerate(open("data/groups")):
        row = row.rstrip()
        group_id, user_id, list_id, permission= row.split("|")

        group = Group(group_id=group_id,
                    user_id=user_id,
                    list_id=list_id,
                    permission=permission
                   )

        # Add to session
        db.session.add(user)

    # Commit work
    db.session.commit()

def load_todo():

    print "To_Do"
    for i, row in enumerate(open("data/todo")):
        row = row.rstrip()
        to_do_id, list_id, item, due_date, status_notdone, todo_location_name, todo_location_address= row.split("|")

        user = User(to_do_id=to_do_id,
                    list_id=list_id,
                    item=item,
                    due_date=due_date,
                    status_notdone=status_notdone,
                    todo_location_name=todo_location_name,
                    todo_location_address=todo_location_address
                    )

        # Add to session
        db.session.add(user)

    # Commit work
    db.session.commit()

def load_shopping():

    print "Shopping"
    for i, row in enumerate(open("data/shopping")):
        row = row.rstrip()
        shopping_id, list_id, item, due_date, status_notdone= row.split("|")

        user = User(shopping_id=shopping_id,
                    list_id=list_id,
                    item=item,
                    due_date=due_date,
                    status_notdone=status_notdone,
                    )

        # Add to session
        db.session.add(user)

    # Commit work
    db.session.commit()


# if __name__ == "__main__":
#     connect_to_db(app)
#     db.create_all()

#     load_users()
#     load_shopping()
#     load_todo()
#     load_groups()
#     load_lists()
