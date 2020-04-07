from datetime import datetime
import urllib.parse
import json
from flask import render_template
from flask import make_response
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for
from dashboard.ssis import monitor
from dashboard import app

# Set app version
version = "0.6.8 (beta)"

# Define routes
@app.route('/')
def index():
    server_name = [*app.config["CONNECTION_STRING"].keys()][0]
    return redirect(url_for('packages', server_name=server_name))

@app.route('/server/<server_name>')
def packages(server_name, folder_name=monitor.all, project_name=monitor.all, status=monitor.all):
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    folder_name = urllib.parse.unquote(folder_name)
    project_name = urllib.parse.unquote(project_name)    

    m = monitor(server_name) if server_name is not None else monitor()
    m.folder_name = folder_name
    m.project_name = project_name
    m.status = status

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'project_name': project_name,
        'folder_name': folder_name,
        'status': status
        }

    engine_folders = m.get_engine_folders()
    engine_projects = m.get_engine_projects()
    engine_kpi = m.get_engine_kpi()
    engine_info = m.get_engine_info()
    execution_statistics = m.get_execution_statistics()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_list = m.get_package_list()
    package_executables = m.get_package_executables()
    package_children = m.get_package_children()
    servers = sorted(app.config["CONNECTION_STRING"].keys())

    return render_template(
        'index.html',
        environment=environment,
        engine_folders=engine_folders,
        engine_projects=engine_projects,
        engine_info=engine_info,
        engine_kpi=engine_kpi,
        execution_statistics=execution_statistics,
        package_info=package_info,
        package_kpi=package_kpi,
        package_list=package_list,
        package_children=package_children,
        package_executables=package_executables,
        servers=servers,
        server_name=server_name
    )

@app.route('/server/<server_name>/folder/<folder_name>/project/<project_name>/status/<status>')
@app.route('/server/<server_name>/folder/<folder_name>/status/<status>')
@app.route('/server/<server_name>/folder/<folder_name>')
@app.route('/folder/<folder_name>/project/<project_name>/status/<status>')
def folder_project_status(server_name=None,folder_name=monitor.all, project_name=monitor.all, status=monitor.all):
    return packages(server_name=server_name,folder_name=folder_name, project_name=project_name, status=status)

@app.route('/server/<server_name>/folder/<folder_name>/project/<project_name>')
@app.route('/folder/<folder_name>/project/<project_name>', defaults={'server_name': None})
def folder_project(server_name,folder_name, project_name):
    return packages(server_name=server_name,folder_name=folder_name, project_name=project_name)

@app.route('/server/<server_name>/folder/<folder_name>')
@app.route('/folder/<folder_name>', defaults={'server_name': None})
def folder(server_name,folder_name):
    return packages(server_name=server_name,folder_name=folder_name)

@app.route('/server/<server_name>/execution/<int:execution_id>')
@app.route('/execution/<int:execution_id>', defaults={'server_name': None})
def execution(server_name, execution_id=0):
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    m = monitor(server_name) if server_name is not None else monitor()
    m.execution_id = execution_id

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'execution_id': execution_id
        }

    engine_folders = m.get_engine_folders()
    engine_projects = m.get_engine_projects()
    engine_kpi = m.get_engine_kpi()
    engine_info = m.get_engine_info()
    execution_statistics = m.get_execution_statistics()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_list = m.get_package_list()
    package_executables = m.get_package_executables()
    package_children = m.get_package_children()

    return render_template(
        'execution-details.html',
        environment=environment,
        engine_folders=engine_folders,
        engine_projects=engine_projects,
        engine_info=engine_info,
        engine_kpi=engine_kpi,
        execution_statistics=execution_statistics,
        package_info=package_info,
        package_kpi=package_kpi,
        package_list=package_list,
        package_children=package_children,
        package_executables=package_executables
    )

@app.route('/server/<server_name>/execution/<int:execution_id>/events/<event_type>')
@app.route('/execution/<int:execution_id>/events/<event_type>', defaults={'server_name': None})
def package_events(server_name, execution_id, event_type):
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    m = monitor(server_name) if server_name is not None else monitor()
    m.execution_id = execution_id

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'execution_id': execution_id,
        'event_type': event_type
        }

    engine_kpi = m.get_engine_kpi()
    engine_info = m.get_engine_info()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_events = m.get_package_events(event_type)

    return render_template(
        'execution-events.html',
        environment=environment,
        engine_info=engine_info,
        package_info=package_info,
        package_kpi=package_kpi,
        package_events=package_events
    )

@app.route('/server/<server_name>/execution/<int:execution_id>/values')
@app.route('/execution/<int:execution_id>/values', defaults={'server_name': None})
def package_execution_values(server_name, execution_id):
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    m = monitor(server_name) if server_name is not None else monitor()
    m.execution_id = execution_id

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'execution_id': execution_id,
        }

    engine_info = m.get_engine_info()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_parameters = m.get_package_details("execution-values")
    package_overrides = m.get_package_details("execution-overrides")

    return render_template(
        'execution-values.html',
        environment=environment,
        engine_info=engine_info,
        package_info=package_info,
        package_kpi=package_kpi,
        package_parameters=package_parameters,
        package_overrides=package_overrides
    )

@app.route('/server/<server_name>/history/<folder_name>/project/<project_name>/status/<status>/package/<package_name>')
@app.route('/history/<folder_name>/project/<project_name>/status/<status>/package/<package_name>')
def package_history(server_name=None, folder_name=monitor.all, project_name=monitor.all, status=monitor.all, package_name=monitor.all):
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    folder_name = urllib.parse.unquote(folder_name)
    project_name = urllib.parse.unquote(project_name)
    package_name = urllib.parse.unquote(package_name)
    
    m = monitor(server_name) if server_name is not None else monitor()
    m.project_name = project_name
    m.package_name = package_name
    m.folder_name = folder_name

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'folder_name': folder_name,
        'project_name': project_name,
        'package_name': package_name,
        'status': status
        }

    engine_kpi = m.get_engine_kpi()
    engine_info = m.get_engine_info()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_history = m.get_package_history()    
    servers = sorted(app.config["CONNECTION_STRING"].keys())

    return render_template(
        'execution-history.html',
        environment=environment,
        engine_info=engine_info,
        package_info=package_info,
        package_kpi=package_kpi,
        package_history=package_history,
        servers=servers,
        server_name=server_name
    )

#@app.route('/ssis/execution-status', methods = ['GET'])
#def get_statuses():
#    execution_status = services.get_package_execution_status()
#    return jsonify ( { 'data': execution_status } )

#@app.route('/<int:execution_id>/execution-history', methods = ['GET'])
#def get_execution_history():
#    history = services.get_package_execution_history()
#    return jsonify ( { 'data': history } )

#@app.route('/ssis/execution-events/<int:execution_id>', methods = ['GET'])
#def get_package_execution_events(execution_id):
#    execution_events = services.get_package_execution_events(execution_id)
#    return jsonify ( { 'data': execution_events } )

#@app.route('/ssis/execution-kpi/<int:execution_id>', methods = ['GET'])
#def get_package_execution_kpi(execution_id):
#    kpi = services.get_package_execution_kpi(execution_id)
#    return jsonify( { 'data': kpi } )

#@app.route('/sample', methods = ['GET'])
#def get_sample():
#    return jsonify({'result': 123})

@app.route('/server/<server_name>/list/packages/<folder>')
@app.route('/server/<server_name>/list/packages')
@app.route('/list/packages')
def list_packages(server_name=None, folder=None):
    
    configFolders = app.config["DEFAULT_SSIS_FOLDERS"] if "DEFAULT_SSIS_FOLDERS" in app.config else None
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    running = monitor(server_name) if server_name is not None else monitor()
    running.folder_name = folder if folder is not None else next(iter(configFolders or []), None)
    running.folder_name = monitor.all if running.folder_name is None else running.folder_name
    running.config.executionCount = 15
    engine_info = running.get_engine_info()    
    running_package_list = running.get_package_list()    

    if folder:
        ssispackages = running.get_ssis_packages_list(folders=[folder])
    else:
        ssispackages = running.get_ssis_packages_list(folders=configFolders)

    return render_template(
        'packages.html',
        environment={
            'version': version,
            'timestamp': datetime.now(),        
            'folder_name': running.folder_name
        },
        engine_info=engine_info,
        package_list=running_package_list,
        ssispackages=ssispackages,
        servers=app.config["CONNECTION_STRING"].keys(),
        server_name=server_name
    )

@app.route('/server/<server_name>/execute/<int:package>', methods=['POST'])
@app.route('/execute/<int:package>', methods=['POST'], defaults={'server_name': None})
def execute_package(server_name, package):
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    parameter = request.form["parameter"]
    m = monitor(server_name) if server_name is not None else monitor()
    m.execute_ssis_package(package, parameter) 
    return redirect(url_for('list_packages'))

@app.route('/server/<server_name>/list/parameternames')
@app.route('/list/parameternames', defaults={'server_name': None})
def list_parameter_names(server_name):
    server_name =  urllib.parse.unquote(server_name) if server_name is not None else [*app.config["CONNECTION_STRING"].keys()][0]
    m = monitor(server_name) if server_name is not None else monitor()
    return json.dumps(m.get_paramter_names()), 200, {'Content-Type': 'application/json; charset=utf-8'}   



@app.errorhandler(404)
def not_found(error):    
    m = monitor()
    engine_info = m.get_engine_info()

    environment = {
        'version': version,
        'timestamp': datetime.now()
        }

    return render_template(
        '404.html',
        environment=environment,
        engine_info=engine_info
    )

