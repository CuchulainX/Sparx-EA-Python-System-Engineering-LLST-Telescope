import os
from flask import Flask, render_template

from lsst.syseng_db import syseng_db_config, get_column_names, get_table_names

app = Flask(__name__)

db_name = os.path.join(syseng_db_config["db_dir"], syseng_db_config["db_name"])

@app.route("/versions")
def display_versions():
    list_of_tables = get_table_names(db_name)
    return render_template("list_template.html", name="Model Versions",
                           input_list=list_of_tables)



if __name__ == "__main__":
    app.run()
