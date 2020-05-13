# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, session, request, flash, jsonify
# from flask_login import login_required, current_user
# from app import login_manager
from jinja2 import TemplateNotFound
from app.base.forms import CreateDatabaseForm
import requests
import logging

log = logging.getLogger(__name__)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


UDAPI_URL = "http://localhost:2020"


@blueprint.route('/index', methods=['GET', 'POST'])
def index():
    # # Initializing all forms for rendering
    createDbForm = CreateDatabaseForm()

    Retriving all the Databases Stored for the user from UDAPI
    url = UDAPI_URL + "/all/databases"
    headers = {'jwtToken': session['jwtToken']}
    response = requests.get(url, headers=headers)
    databasesResp = response.json()
    if databasesResp['success']:
        session['count_DBs'] = len(databasesResp['mysql']) + len(databasesResp['mongodb'])
        session['count_SQL'] = len(databasesResp['mysql'])
        session['count_noSQL'] = len(databasesResp['mongodb'])
    else:
        print(user_data['message'])
        return render_template('errors/page_500.html'), 500

    # Retrive all EntitySets of each Databases
    databaseTypes = ['mysql', 'mongodb']
    databases = []
    for databaseType in databaseTypes:
        for databaseName in databasesResp[databaseType]:
            url = UDAPI_URL + '/' + databaseType + '/databases/' + databaseName
            headers = {'jwtToken': session['jwtToken']}
            response = requests.get(url, headers=headers)
            entitySetsResp = response.json()
            if entitySetsResp['success']:
                database = {
                    "name": databaseName,
                    "type": databaseType,
                    "entitySets": entitySetsResp['entitySets']
                }
                databases.append(database)
            else:
                print(user_data['message'])
                return render_template('errors/page_500.html'), 500

    # databases = [{"name": "test-student", "type": "mysql", "entitySets": ['professors', 'lizards', 'mimosas']}, {"name": "test2", "type": "mongo", "entitySets": ['swords', 'reverse']}, {"name": "test3", "type": "mongo", "entitySets": ["Lorem", "ipsum", "dolor"]},
    #              {"name": "test-student", "type": "mysql", "entitySets": ['professors', 'lizards', 'mimosas']}, {"name": "test2", "type": "mongo", "entitySets": ['bread', 'swords']}, {"name": "test3", "type": "mongo", "entitySets": ["Lorem", "ipsum", "dolor"]}]

    # Creating new Database by sending request to UDAPI
    if 'createDB' in request.form:
        database_type = request.form['database_type']
        database_name = request.form['database_name']

        url = UDAPI_URL + "/" + database_type + "/databases"
        payload = {
            "databaseName":database_name
        }
        headers = {'jwtToken': session['jwtToken']}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data['success']:
            flash(data["message"], "success")
            return redirect(url_for('home_blueprint.index'))
        elif not data['success']:
            flash("You can't have two databases with the same name and type.", "danger")
            return redirect(url_for('home_blueprint.index'))
            
        print(data['message'])
        return render_template('errors/page_500.html'), 500

    return render_template('index.html', databases=databases, createDbForm=createDbForm)


@blueprint.route('/<template>')
def route_template(template):

    if not "username" in session:
        return redirect(url_for('base_blueprint.login'))

    # if not current_user.is_authenticated:
    #     return redirect(url_for('base_blueprint.login'))
    # return render_template(template + '.html')
    try:

        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('error-404.html'), 404

    except:
        return render_template('error-500.html'), 500


@blueprint.app_errorhandler(404)
def handle_exceptions(e):
    return render_template('error-404.html'), 404

@blueprint.app_errorhandler(Exception)
def handle_unexpected_error(e):
    msg = "UnexpectedError: " + str(e)
    log.exception(f"{bcolors.FAIL}{msg}{bcolors.WARNING}")
    print(f"{bcolors.ENDC}")
    return render_template('error-500.html'), 500

