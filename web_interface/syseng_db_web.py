import os
from flask import Flask, render_template, request

from lsst.syseng_db import syseng_db_config, get_table_names
from lsst.syseng_db import keyword_query, get_parameter_names

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
        name_list = get_parameter_names(db_name, model_version)

    return render_template("parameter_name_search_form.html",
                           model_version=model_version,
                           input_list=name_list)


@app.route("/search", methods=['POST', 'GET'])
def search_params():
    result_param_list = []
    if request.method == 'POST':
        kwrd = request.form['keyword'].replace(' ','').split(',')
        vv = request.form['version']
        result_param_list = keyword_query(db_name, vv, kwrd)

    return render_template("keyword_search_form.html",
                           input_list=result_param_list)


@app.route("/")
def index():
    return render_template("main_page.html")

if __name__ == "__main__":
    app.run()
