from flask import Flask
app= Flask(__name__)
app.secret_key ="sneaky"
DATABASE = "rec_schema"