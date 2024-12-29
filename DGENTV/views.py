from flask import Blueprint, render_template, request, jsonify
import requests

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("homepage.html")

@views.route('/stats', methods=['GET'])
def get_affiliate_stats():
    # ... your route logic here ...
    return "Some response"