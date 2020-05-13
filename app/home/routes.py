# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, session
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.base.forms import CreateDatabaseForm


@blueprint.route('/index')
def index():
    # if not "username" in session:
    #     return redirect(url_for('base_blueprint.login'))
    createDbForm = CreateDatabaseForm()
    databases = [{"name": "test-student", "type": "mysql", "entitySets": ['professors', 'lizards', 'mimosas']}, {"name": "test2", "type": "mongo", "entitySets": ['swords', 'reverse']}, {"name": "test3", "type": "mongo", "entitySets": ["Lorem", "ipsum", "dolor"]},
                 {"name": "test-student", "type": "mysql", "entitySets": ['professors', 'lizards', 'mimosas']}, {"name": "test2", "type": "mongo", "entitySets": ['bread', 'swords']}, {"name": "test3", "type": "mongo", "entitySets": ["Lorem", "ipsum", "dolor"]}]
    return render_template('index.html', databases=databases, createDbForm=createDbForm)

    # if not current_user.is_authenticated:
    #     return redirect(url_for('base_blueprint.login'))
    # databases=[{"name":"test-student", "type":"mysql"},{"name":"test2", "type":"mongo"},{"name":"test3", "type":"mongo"},{"name":"test4", "type":"mysql"},{"name":"joan","type":"mongo"},{"name":"test4", "type":"mysql"},{"name":"joan","type":"mongo"}]
    # return render_template('index.html', databases=databases)


@blueprint.route('/<template>')
def route_template(template):

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    try:

        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('error-404.html'), 404

    except:
        return render_template('error-500.html'), 500
