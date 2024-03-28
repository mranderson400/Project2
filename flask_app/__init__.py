from flask import Flask
app = Flask(__name__)
app.secret_key = "is it really a secret tho"
DATABASE = 'sights'
# drop init folder in flask app
