import os
import sqlite3
from collections import OrderedDict
from flask import Flask, render_template, request

from lsst.syseng_db import syseng_db_config, get_table_names
from lsst.syseng_db import keyword_query, get_parameter_names
from lsst.syseng_db import get_xml_files

app = Flask(__name__)


db_name = os.path.join(syseng_db_config["db_dir"], syseng_db_config["db_name"])


@app.route("/list-names", methods=['POST', 'GET'])
def list_param_names():
    name_list = []
    list_of_versions = get_table_names(db_name)
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
                           input_list=name_list,
                           available_versions=list_of_versions,
                           selected_version=model_version)


@app.route("/list-xml-files", methods=['POST', 'GET'])
def list_xml_files():
    name_list = []
    list_of_versions = get_table_names(db_name)
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
                           input_list=name_list,
                           available_versions=list_of_versions)


@app.route("/key_numbers", methods=['POST', 'GET'])
def generate_key_numbers():
    version = None
    param_list = []
    list_of_versions = get_table_names(db_name)
    if request.method == 'POST':
        version = str(request.form['version'])

        if version == '':
            message = "You must specify a model version to query." \
                      +" Try clicking the 'List all available model versions'" \
                      +" button on the main page."
            return render_template("error_template.html",
                                   message=message)

        param_name_map = OrderedDict()
        param_name_map['etendueRec'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['FieldOfView'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['m1OuterCa'] = 'Telescope Requirements_v1.xml'
        param_name_map['effAperture'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['minPixelSize'] = 'Science_Requirements_v1.xml'
        param_name_map['pixelSize'] = 'OSS_Detail_OpticalSystem_v1.xml'
        param_name_map['visitExpTime'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['nVisitExp'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['slewSettle_time'] = 'Telescope Requirements_v1.xml'
        param_name_map['nCalibExpDay'] = 'OSS_Detail_ScienceBulkData_v1.xml'
        param_name_map['PixelPitch'] = 'Camera Requirements_v1.xml'
        param_name_map['camDynamicRange'] = 'Camera Requirements_v1.xml'
        param_name_map['DRT1'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['drProcessingPeriod'] = 'Data Management Requirements_v1.xml'
        param_name_map['uNomRed_50'] = 'Camera Requirements_v1.xml'
        param_name_map['uNomBlue_50'] = 'Camera Requirements_v1.xml'
        param_name_map['gNomRed_50'] = 'Camera Requirements_v1.xml'
        param_name_map['gNomBlue_50'] = 'Camera Requirements_v1.xml'
        param_name_map['rNomRed_50'] = 'Camera Requirements_v1.xml'
        param_name_map['rNomBlue_50'] = 'Camera Requirements_v1.xml'
        param_name_map['iNomRed_50'] = 'Camera Requirements_v1.xml'
        param_name_map['iNomBlue_50'] = 'Camera Requirements_v1.xml'
        param_name_map['zNomRed_50'] = 'Camera Requirements_v1.xml'
        param_name_map['zNomBlue_50'] = 'Camera Requirements_v1.xml'
        param_name_map['yNomRed_50'] = 'Camera Requirements_v1.xml'
        param_name_map['yNomBlue_50'] = 'Camera Requirements_v1.xml'
        param_name_map['nAlertNightAvg'] = 'OSS_Issues.xml'
        param_name_map['OTT1'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['Asky'] = 'Science_Based_System_Requirements_v1.xml'
        param_name_map['Nv1Sum'] = 'Science_Based_System_Requirements_v1.xml'

        for name in param_name_map:
            try:
                results = keyword_query(db_name, version, [name],
                                        xml_list=[param_name_map[name]])

            except sqlite3.OperationalError, w:
                return render_template("error_template.html",
                                       message=w.message)


            for pp in results:
                if pp.name==name:
                    param_list.append(pp)

    return render_template("key_numbers.html",
                           version=version,
                           input_list=param_list,
                           available_versions=list_of_versions)



@app.route("/search", methods=['POST', 'GET'])
def search_params():
    result_param_list = []
    list_of_versions = get_table_names(db_name)
    kwrd = None
    version = None
    xml_list = None
    if request.method == 'POST':
        kwrd = [str(ww) for ww in request.form['keyword'].replace(' ','').split(',')]
        version = request.form['version']
        xml_list = [str(ww.lstrip().rstrip()) for ww in request.form['xml_list'].split(',')]
        print xml_list

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
                           xml_list=xml_list,
                           available_versions=list_of_versions)


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
    return render_template("main.html")

if __name__ == "__main__":
    app.run()
