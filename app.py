from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import general_routes
import ingredient_routes
import recipes_routes
import user_routes
