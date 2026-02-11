from flask import Blueprint, render_template
from . import home_page

@home_page.route("/")
def index():
    return render_template('base.html')


