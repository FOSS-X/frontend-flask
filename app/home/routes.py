# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, session
# from flask_login import login_required, current_user
# from app import login_manager
from jinja2 import TemplateNotFound
import requests

UDAPI_URL = "http://localhost:2020"



@blueprint.route('/index')
def index():
    if not "username" in session:
        return redirect(url_for('base_blueprint.login'))
    

    # Retriving all the Databases Stored for the user from UDAPI
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
            entitySetsResp =response.json()
            if entitySetsResp['success']:
                database = {
                    "name":databaseName,
                    "type":databaseType,
                    "entitySets":entitySetsResp['entitySets']
                }
                databases.append(database)
            else:
                print(user_data['message'])
                return render_template('errors/page_500.html'), 500
            print(databases)

    # databases=[{"name":"test-student", "type":"mysql","entitySets":['professors','lizards','mimosas']},{"name":"test2", "type":"mongo","entitySets":['swords','reverse']},{"name":"test3", "type":"mongo","entitySets":["Lorem", "ipsum", "dolor"]},{"name":"test-student", "type":"mysql","entitySets":['professors','lizards','mimosas']},{"name":"test2", "type":"mongo","entitySets":['bread','swords']},{"name":"test3", "type":"mongo","entitySets":["Lorem", "ipsum", "dolor"]}]
    return render_template('index.html', databases=databases)

    # if not current_user.is_authenticated:
    #     return redirect(url_for('base_blueprint.login'))
    # databases=[{"name":"test-student", "type":"mysql"},{"name":"test2", "type":"mongo"},{"name":"test3", "type":"mongo"},{"name":"test4", "type":"mysql"},{"name":"joan","type":"mongo"},{"name":"test4", "type":"mysql"},{"name":"joan","type":"mongo"}]
    # return render_template('index.html', databases=databases)

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
