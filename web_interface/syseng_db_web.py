import os
import sqlite3
from flask import Flask, render_template, request

from lsst.syseng_db import syseng_db_config, get_table_names
from lsst.syseng_db import keyword_query, get_parameter_names
from lsst.syseng_db import get_xml_files

app = Flask(__name__)

db_name = os.path.join(syseng_db_config["db_dir"], syseng_db_config["db_name"])

@app.route("/versions", methods=['POST', 'GET'])
def display_versions():
    list_of_tables = get_table_names(db_name)
    return render_template("list_template.html", name="Model Versions",
                           input_list=list_of_tables)


@app.route("/list-names", methods=['POST', 'GET'])
def list_param_names():
    name_list = []
    model_version = None
    if request.method == 'POST':
        model_version = request.form['version']

        if model_version == '':
            message = "You must specify a model version to query." \
                      +" Try clicking the 'List all available model versions'" \
                      +" button on the main page."
            return render_template("error_template.html",
                                   message=message)

        try:
            name_list = get_parameter_names(db_name, model_version)
        except sqlite3.OperationalError, w:
            return render_template("error_template.html",
                                   message=w.message)

    return render_template("parameter_name_search_form.html",
                           model_version=model_version,
                           input_list=name_list)


@app.route("/list-xml-files", methods=['POST', 'GET'])
def list_xml_files():
    name_list = []
    model_version = None
    if request.method == 'POST':
        model_version = request.form['version']

        if model_version == '':
            message = "You must specify a model version to query." \
                      +" Try clicking the 'List all available model versions'" \
                      +" button on the main page."
            return render_template("error_template.html",
                                   message=message)

        try:
            name_list = get_xml_files(db_name, model_version)
        except sqlite3.OperationalError, w:
            return render_template("error_template.html",
                                   message=w.message)

    return render_template("xml_file_search_form.html",
                           model_version=model_version,
                           input_list=name_list)



@app.route("/search", methods=['POST', 'GET'])
def search_params():
    result_param_list = []
    kwrd = None
    version = None
    xml_list = None
    if request.method == 'POST':
        kwrd = [str(ww) for ww in request.form['keyword'].replace(' ','').split(',')]
        version = request.form['version']
        xml_list = [str(ww) for ww in request.form['xml_list'].split(',')]

        if len(xml_list)==1 and xml_list[0]=='':
            xml_list = None

        if version == '':
            message = "You must specify a model version to query." \
                      +" Try clicking the 'List all available model versions'" \
                      +" button on the main page."
            return render_template("error_template.html",
                                   message=message)

        try:
            result_param_list = keyword_query(db_name, version, kwrd,
                                              xml_list=xml_list)
        except sqlite3.OperationalError, w:
            return render_template("error_template.html",
                                   message=w.message)

    return render_template("keyword_search_form.html",
                           input_list=result_param_list,
                           keyword_list=kwrd,
                           version=version,
                           xml_list=xml_list)


@app.route("/optical_system", methods=['POST', 'GET'])
def get_optical_system():

    result_param_list = []
    title = None
    xml_list = ['OSS_Detail_OpticalSystem_v1.xml', 'Telescope Requirements_v1.xml',
                 'Camera Requirements_v1.xml']
    if request.method == 'POST':
        kwrd = [str(request.form['element'])]
        title = kwrd[0]
        result_param_list = keyword_query(db_name, 'v_0_0', kwrd, xml_list=xml_list)

    return render_template("optical_system.html", input_list=result_param_list, title=title)


@app.route("/")
def index():
    return render_template("main_page.html")

if __name__ == "__main__":
    app.run()
