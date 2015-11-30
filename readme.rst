================================================
`Nucleus`
================================================

Keeping your home & family organized can be tough with everyone on the go. Nucleus makes planning easier by allowing users to create grocery, shopping, and to-do lists and share them with other users. With flexible permissions, allowed users can edit lists and mark off completed items, and Nucleus will automatically notify everyone else on the list through SMS messaging. When users are near the location of a list, they're sent a reminder to take care of it. Nucleus helps you manage your busy life.

Features:
---------


Tech Stack:
-----------
- Python
- SQLite relational databases
- SQLAlchemy Object Relational Mapper
- Flask web framework
- Jinja templating
- Javascript
- jQuery
- AJAX 
- JSON
- CSS + Bootstrap
- Testing with unittest
- Twilio API, Geopy library, ngrok

Running Nucleus Locally:

Create a virtual environment 

```
> virtualenv env
> source env/bin/activate
```

Install requirements

```
> pip install -r requirements.txt
```

Run the app 

```
> python server.py
```


Open your browser and navigate to 

```
http://localhost:5000/
```

Note: A Twilio account (set as 'TWILIO_ACCOUNT_SID'), authorization token (set as 'TWILIO_AUTH_TOKEN'), and phone number (set as 'TWILIO_NUMBER' are required to run this app. Add them to a secrets.sh file.

```
> source secrets.sh
```
