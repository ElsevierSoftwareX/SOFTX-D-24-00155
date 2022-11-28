###############################################################################################
# OSLiFe-DiSC describes OSI approved Open Source Licenses through Features (legal terms)
# according to a unified model It allows to Discover each license and understand it, to Select
# licenses satisfying a set of features and Compare two licenses to highlight the differences.
###############################################################################################

# This file is part of OSLiFe-DiSC -
# Copyright © 2022 Sihem Ben Sassi
#
# OSLiFe-DiSC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# OSLiFe-DiSC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License, version 3 for more details.
#
# You should have received a copy of the GNU Affero General Public License,
# version 3 along with OSLiFe-DiSC. If not, see <http://www.gnu.org/licenses/>.


#import pathlib
from flask import Flask
# import xml.etree.ElementTree as et
# import requests
# from bs4 import BeautifulSoup as bs
# from anytree import Node
# from flask import Blueprint, render_template, request, flash, jsonify
# from werkzeug.utils import redirect
# from connection import *
from .views import *



BASE_DIR = pathlib.Path(__file__).resolve().parent
DIR_RES = BASE_DIR / "resultat"

web_app = Flask(__name__)
web_app.config['SECRET_KEY'] = 'lkjhgtrese gfrdeqzq'
web_app.register_blueprint(views)
def connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Osl123disc",
        database = "oslicenses"
    )
    mycursor = conn.cursor()
    return (conn,mycursor)


