# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, session, request, flash,jsonify
# from flask_login import login_required, current_user
# from app import login_manager
from jinja2 import TemplateNotFound
from app.base.util import *
from app.base.forms import CreateDatabaseForm, UpdateEntitySetForm
import requests
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@blueprint.route('/index', methods=['GET', 'POST'])
@verify_user
def index():
    # Initializing all forms for rendering
    createDbForm = CreateDatabaseForm()
    updateESForm = UpdateEntitySetForm()

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
        print(databasesResp['message'])
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

    # Creating new Database by sending request to UDAPI
    if 'createDB' in request.form:
        database_type = request.form['database_type']
        database_name = request.form['database_name']

        url = UDAPI_URL + "/" + database_type + "/databases"
        payload = {"databaseName":database_name}
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

    # Deleteing a Database
    if 'deleteDB' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')

        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name
        headers = {'jwtToken': session['jwtToken']}
        response = requests.delete(url, headers=headers)
        data = response.json()

        if data['success']:
            flash(data['message'], "success")
            return redirect(url_for('home_blueprint.index'))
        elif not data['success']:
            flash(data['message'], "danger")
            return redirect(url_for('home_blueprint.index'))
        print(data['message'])
        return render_template('errors/page_500.html'), 500
 
    # Create a new Enity Set
    if 'createEntitySet' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')
        entitySetName = request.form['entitySetName']
        attributes_data = request.form['create-es-attributes']

        payload = json.loads(attributes_data)
        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name
        headers = {'jwtToken': session['jwtToken']}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data['success']:
            flash(data["message"], "success")
            return redirect(url_for('home_blueprint.index'))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.index'))

        print(data['message'])
        return render_template('errors/page_500.html'), 500

    # rename an existing entity Set
    if 'updateEntitySet' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')
        entitySetName = request.args.get('entitySetName')
        newEntitySetName = request.form['entitySet_name']

        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name + "/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        payload = {"newEntitySetName": newEntitySetName}
        response = requests.put(url, headers=headers, json=payload)
        data = response.json()

        if data['success']:
            flash(f"From {database_type} database: '{database_name}', Entity Set Renamed from:      {entitySetName} --> {newEntitySetName}", "success")
            return redirect(url_for('home_blueprint.index'))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.index'))

        print(data['message'])
        return render_template('errors/page_500.html'), 500

    # Delete Enity Set
    if 'deleteEntitySet' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')
        entitySetName = request.args.get('entitySetName')

        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name + "/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        response = requests.delete(url, headers=headers)
        data = response.json()
        
        if data['success']:
            flash(f"From {database_type} database: '{database_name}', Entity Set: '{entitySetName}' deleted successfully", "success")
            return redirect(url_for('home_blueprint.index'))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.index'))

        print(data['message'])
        return render_template('errors/page_500.html'), 500

    return render_template('index.html', databases=databases, createDbForm=createDbForm, updateESForm=updateESForm)

# @blueprint.route('/index', methods=['GET', 'POST'])
# def index():
#     createDbForm = CreateDatabaseForm()
#     updateESForm = UpdateEntitySetForm()
#     databases = [{"name": "test-student", "type": "mysql", "entitySets": ['professors', 'lizards', 'mimosas']}, {"name": "test2", "type": "mongo", "entitySets": ['swords', 'reverse']}, {"name": "test3", "type": "mongo", "entitySets": ["Lorem", "ipsum", "dolor"]},
#                  {"name": "test-student", "type": "mysql", "entitySets": ['professors', 'lizards', 'mimosas']}, {"name": "test2", "type": "mongo", "entitySets": ['bread', 'swords']}, {"name": "test3", "type": "mongo", "entitySets": ["Lorem", "ipsum", "dolor"]}]
#     return render_template('index.html', databases=databases, createDbForm=createDbForm, updateESForm=updateESForm)


@blueprint.route('/entity_sets/<databaseType>/<databaseName>/<entitySetName>', methods=['GET', 'POST'])
@verify_user
def displayES(databaseType,databaseName,entitySetName):
    updateESForm = UpdateEntitySetForm()

    #get the following data from API in this format
    url = UDAPI_URL + "/" + databaseType + "/databases/" + databaseName 
    headers = {'jwtToken': session['jwtToken']}
    response = requests.get(url, headers=headers)
    entitySetsData = response.json()

    if entitySetsData['success']:
        entitySets = entitySetsData['entitySets']
        database = {
            "name":databaseName,
            "type":databaseType,
            "entitySets":entitySets
        }

    # else:
    #     print(f"{bcolors.FAIL}Exception from UDAPI server side: {entitySetsData['message']}{bcolors.ENDC}")
    #     return render_template('errors/page_500.html'), 500

    # database = {"name": "Test", "type": "MongoDB",
    #             "entitySets": ["uno", "dos", "tres", "four", "five"]}
    
    # Create a new Enity Set
    if 'createEntitySet' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')
        entitySetName = request.form['entitySetName']
        attributes_data = request.form['create-es-attributes']

        payload = json.loads(attributes_data)
        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name
        headers = {'jwtToken': session['jwtToken']}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data['success']:
            flash(data["message"], "success")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName="None"))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName="None"))

        print(data['message'])
        return render_template('errors/page_500.html'), 500

    
    # rename an existing entity Set
    if 'updateEntitySet' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')
        entitySetName = request.args.get('entitySetName')
        newEntitySetName = request.form['entitySet_name']

        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name + "/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        payload = {"newEntitySetName": newEntitySetName}
        response = requests.put(url, headers=headers, json=payload)
        data = response.json()

        if data['success']:
            flash(f"From {database_type} database: '{database_name}', Entity Set Renamed from:      {entitySetName} --> {newEntitySetName}", "success")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName="None"))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName="None"))

        print(data['message'])
        return render_template('errors/page_500.html'), 500

    # Delete Enity Set
    if 'deleteEntitySet' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')
        entitySetName = request.args.get('entitySetName')

        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name + "/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        response = requests.delete(url, headers=headers)
        data = response.json()
        
        if data['success']:
            flash(f"From {database_type} database: '{database_name}', Entity Set: '{entitySetName}' deleted successfully", "success")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName="None"))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName="None"))

        print(data['message'])
        return render_template('errors/page_500.html'), 500

    # Get entities for the table
    # If entityset selected is not None and is in entity Sets of the DatabaseName
    entitySet={}
    if entitySetName in entitySets:
        url = UDAPI_URL + "/" + databaseType + "/databases/" + databaseName + "/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        response = requests.get(url, headers=headers)
        entitiesData = response.json()

        url = UDAPI_URL + "/" + databaseType + "/databases/" + databaseName + "/schema/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        response = requests.get(url, headers=headers)
        schemaObj=response.json()
        
        if entitiesData['success']:
            entities = entitiesData['message']
            entitySet = {
                "name":entitySetName,
                "schema":schemaObj["schema"],
                "primary_key":schemaObj["primary_key"]
            }
            if entities:
                entitySet["records"]=entities
            else:
                entitySet["records"]="";
            print(entitySet)
        elif not entitiesData['success']:
            flash(entitiesData["message"], "danger")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName=entitySetName))
    else:
        entities = None

    
    # if 'createEntity' in request.form:
        # return entitiesData
    
    # if entitySetName == "None":
    #     entities = {
    #         "name": "uno",
    #         "records": [
    #             {"id": "ipsum", "name": "amet", "course": "captain"},
    #             {"id": "morrison", "name": "frog", "course": "dinner"}
    #         ],
    #         "schema": {"id": "integer", "name": "string", "course": "string"},
    #         "primary_key": "id"
    #     }
    # else:
    #     entities = {
    #         "name": "dos",
    #         "records": [
    #             {"id": "ipsum", "name": "amet", "course": "captain","courses": "captaisn"},
    #             {"id": "morrison", "name": "frog", "course": "dinner"}
    #         ],
    #         "schema": {"id": "integer", "name": "string", "course": "string"},
    #         "primary_key": "id"
    #     }

    # Create an Entity
    if 'createNewEntity' in request.form:
        database_type = request.args.get('databaseType')
        database_name = request.args.get('databaseName')
        entitySetName = request.args.get('entitySetName')
        print(entitySetName)
        formData=request.form.to_dict()
        entityObj={}
        entityObj["entity"]={}
        for attribute,value in formData.items():
            if attribute != 'createNewEntity':
                entityObj["entity"][attribute]=value
        
        payload = json.loads(json.dumps(entityObj))
        url = UDAPI_URL + "/" + database_type + "/databases/" + database_name + "/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        if data['success']:
            flash(data["message"], "success")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName=entitySetName))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName=entitySetName))

        print(data['message'])
        return render_template('errors/page_500.html'), 500

    # Update an Entity
    # if 'updateEntity' in request.form:
    #     # database_type = request.args.get('databaseType')
    #     # database_name = request.args.get('databaseName')
    #     # entitySetName = request.args.get('entitySetName')


    #     url = UDAPI_URL + "/" + databaseType + "/databases/" + databaseName + "/schema/" + entitySetName
    #     headers = {'jwtToken': session['jwtToken']}
    #     response = requests.get(url, headers=headers)
    #     schemaObj=response.json()

    #     keyAttribute = schemaObj['primary_key']
    #     # return (schemaObj)
    #     url = UDAPI_URL + "/" + databaseType + "/databases/" + databaseName + "/" + entitySetName + "/" + keyAttribute
    #     headers = {'jwtToken': session['jwtToken']}
    #     payload = {
    #         "primeAttributeValue": "12",
    #         "attributeName": "dname",
    #         "attributeValue": "Data Science"
    #     }
    #     response = requests.put(url, headers=headers, json=payload)
    #     data = response.json()

    #     return data


    # Delete Entity
    if 'deleteEntity' in request.form:
        keyAttributeValue = request.args.get('keyAttributeValue')

        url = UDAPI_URL + "/" + databaseType + "/databases/" + databaseName + "/schema/" + entitySetName
        headers = {'jwtToken': session['jwtToken']}
        response = requests.get(url, headers=headers)
        schemaObj=response.json()


        keyAttribute = schemaObj['primary_key']
        url = UDAPI_URL + "/" + databaseType + "/databases/" + databaseName + "/" + entitySetName + "/" + keyAttribute
        headers = {'jwtToken': session['jwtToken']}
        payload = {
            "primeAttributeValue":keyAttributeValue
        }
        response = requests.delete(url, headers=headers, json=payload)
        data = response.json()

        if data['success']:
            flash(data["message"], "success")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName=entitySetName))
        elif not data['success']:
            flash(data["message"], "danger")
            return redirect(url_for('home_blueprint.displayES', databaseType=databaseType, databaseName=databaseName, entitySetName=entitySetName))

        print(data['message'])
        return render_template('errors/page_500.html'), 500



    try:
        return render_template('entity_sets.html', database=database, entitySet=entitySet, updateESForm=updateESForm)
    except TemplateNotFound:
        return render_template('error-404.html'), 404


@blueprint.route('/<template>')
def route_template(template):
    try:
        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('error-404.html'), 404

    except:
        return render_template('error-500.html'), 500
