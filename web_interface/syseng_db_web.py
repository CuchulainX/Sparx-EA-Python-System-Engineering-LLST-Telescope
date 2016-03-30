import os
from flask import Flask, render_template, request

from lsst.syseng_db import syseng_db_config, get_table_names
from lsst.syseng_db import keyword_query

app = Flask(__name__)

db_name = os.path.join(syseng_db_config["db_dir"], syseng_db_config["db_name"])

@app.route("/versions")
def display_versions():
    list_of_tables = get_table_names(db_name)
    return render_template("list_template.html", name="Model Versions",
                           input_list=list_of_tables)

@app.route("/search", methods=['POST', 'GET'])
def search_params():
    results = []
    if request.method == 'POST':
        kwrd = request.form['keyword']
        vv = request.form['version']
        result_param_list = keyword_query(db_name, vv, [kwrd])
        for rr in result_param_list:
            results.append(rr.name)

    return render_template("search_form.html", input_list=results)


if __name__ == "__main__":
    app.run()
