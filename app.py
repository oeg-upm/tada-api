from tada_hdt_entity.entity import EntityAnn
from tada_hdt_entity.parser import Parser
from tada_hdt_entity.entity import deref_list_string
import csv
from flask import Flask, request, jsonify, render_template, redirect, Response
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from flasgger import swag_from, Swagger, validate
import traceback

try:
    import simplejson as json
except ImportError:
    import json

try:
    from http import HTTPStatus
except ImportError:
    import httplib as HTTPStatus


import sys
import os
import logging
import util


rdfs_label = "http://www.w3.org/2000/01/rdf-schema#label"
labels = ["http://www.w3.org/2000/01/rdf-schema#label",
          "http://www.w3.org/2004/02/skos/core#prefLabel",
          "http://purl.obolibrary.org/obo/IAO_0000118"
]

def set_config(logger, logdir=""):
    if logdir != "":
        handler = logging.FileHandler(logdir)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'TADA APIs',
    # 'uiversion': 3,
    # 'openapi': '3.0.2',
    #  'doc_dir': './'
}

BASE_DIR = os.path.dirname(app.instance_path)
logger = logging.getLogger(__name__)
logger_dir = os.path.join(BASE_DIR, "web.log")
set_config(logger, logger_dir)

# swagger = Swagger(app, validation_error_handler=validation_error_inform_error)
swagger = Swagger(app)
UPLOAD_DIR = os.path.join(BASE_DIR, 'upload')
SOURCES_DIR = os.path.join(BASE_DIR, 'sources.csv')


def validation_error_inform_error(err, data, schema):
    """
    Custom validation error handler which produces 404 Bad Request
    response in case validation fails and returns the error
    """
    print("In validation_error_inform_error> ")
    print(str(err))
    abort(Response(
        json.dumps({'error': str(err), 'data': data, 'schema': schema}),
        status=HTTPStatus.BAD_REQUEST))


def custom_validation_function(data, schema):
    """
    """
    print("data: ")
    print(data)
    print("schema: ")
    print(schema)


@app.route('/')
def hello_world():
    return redirect('/apidocs')


@app.route('/subject', methods=['POST'])
@swag_from('subject.yml')
def annotate_subject_col():
    logger.debug("annotate_subject_col> form data: ")
    logger.debug(request.form)
    col_id = int(request.form['col_id'])
    source_file = request.files['source']
    if 'alpha' in request.form:
        alpha = float(request.form['alpha'])
    else:
        alpha = 0.9
    if 'ann_source' not in request.form:
        return jsonify(error="ann_source is not passed"), 500
    annotation_source_id = request.form['ann_source']
    uploaded_dir = save_file(source_file)
    if uploaded_dir:
        hdt_source = get_hdt_source(annotation_source_id)
        print("hdt source: %s" % hdt_source["source"])
        ea = EntityAnn(hdt_source["source"], "entity.log", alpha)
        ea.clear_label_uri()

        for lab in labels:
            ea.append_label_uri(lab)

        parser = Parser(uploaded_dir)
        data = parser.parse_vertical()

        for lan_tag in ["@en", ""]:
            ea.set_language_tag(lan_tag)
            ea.set_title_case(True)
            print("col_id: %d" % col_id)

            entities_ptr = ea.annotate_column(data, col_id, True, True)
            entities = [str(e) for e in entities_ptr]
            thing = 'http://www.w3.org/2002/07/owl#Thing'
            c_entities = []
            black_list_uris = get_black_list()
            for e in entities:
                if e not in black_list_uris:
                    c_entities.append(e)
                else:
                    print("ignore blacklist: "+e)
            entities = c_entities

            if 'k' in request.form:
                k = int(request.form['k'])
                entities = entities[:k]
            j = {
                "entities": entities,
            }
            if len(entities) > 0:
                print("Breaking")
                break
            else:
                print("No entities")
        return jsonify(j)
    else:
        return jsonify(error="error saving the uploaded file"), 500


@app.route('/property', methods=['POST'])
@swag_from('property.yml',)
def annotate_property_col():
    logger.debug("annotate_property_col> form data: ")
    logger.debug(request.form)
    col_id = int(request.form['subject_col_id'])
    source_file = request.files['source']

    if 'k' in request.form:
        k = int(request.form['k'])
    else:
        k = None

    if 'class_uri' in request.form:
        class_uri = request.form['class_uri']
    else:
        class_uri = None

    if 'ann_source' not in request.form:
        return jsonify(error="ann_source is not passed"), 500
    annotation_source_id = request.form['ann_source']

    uploaded_dir = save_file(source_file)
    if uploaded_dir:
        hdt_source = get_hdt_source(annotation_source_id)
        ea = EntityAnn(hdt_source["source"], "entity.log")
        ea.set_title_case(True)
        parser = Parser(uploaded_dir)
        data = parser.parse_vertical()
        headers = util.get_headers_csv(uploaded_dir)
        pairs = []
        for prop_id, col_header in enumerate(headers):
            if prop_id==col_id: # if subject column
                j = {'header': col_header, 'properties': [rdfs_label]}
                pairs.append(j)
                continue

            for lan_tag in ["@en", ""]:
                ea.set_language_tag(lan_tag)
                properties_ptr = ea.annotate_entity_property_column(data, col_id, prop_id)

                if len(properties_ptr) == 0 and class_uri is not None:
                    properties_ptr = ea.annotate_entity_property_heuristic(data, class_uri, prop_id)

                properties = [str(p) for p in properties_ptr]

                if k is not None:
                    properties = properties[:k]

                j = {'header': col_header, 'properties': properties}
                pairs.append(j)

                # if len(properties) > 0:
                #     break

        return jsonify({'cols_properties': pairs})
    else:
        j = {"Error saving the uploaded file"}
        return jsonify(error="error saving the uploaded file"), 500


def save_file(sourcefile):
    if sourcefile.filename != "":
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        filename = secure_filename(sourcefile.filename)
        uploaded_file_dir = os.path.join(UPLOAD_DIR, filename)
        sourcefile.save(uploaded_file_dir)
        return uploaded_file_dir
    else:
        return None


def get_black_list():
    """
    :return:
    """
    uris = []
    try:
        bl_dir = os.path.join(BASE_DIR, "blacklist.csv")
        f = open(bl_dir)
        for line in f.readlines():
            uris.append(line)
        f.close()
    except:
        print("Exception: blacklist.csv is not found in: "+bl_dir)
    return uris


def get_hdt_source(source_id):
    """
    Get source
    """
    sources = load_sources()
    for s in sources:
        if s["id"] == source_id:
            return s
    print("get_hdt_source> source <%s> is not found" % source_id)
    return ""


def load_sources():
    """
    Retrieve the sources from the sources.csv
    """
    sources = []
    # For automated tests
    if not SOURCES_DIR:
        d = { "id": "test", "name": "test", "type": "HDT", "source": os.environ['test_hdt_dir']}
        return [d]
        # os.environ['test_hdt_dir']
    # For normal usage (local or production)
    if os.path.exists(SOURCES_DIR):
        with open(SOURCES_DIR, 'r') as data:
            for line in csv.DictReader(data):
                print(line)
                sources.append(line)
    else:
        print("%s is not found" % SOURCES_DIR)
    return sources


@app.route('/sources', methods=['GET'])
@swag_from('sources.yml',)
def get_sources():
    sources = load_sources()
    for s in sources:
        del s["source"]
    return jsonify(sources=sources), 200


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        app.run(debug=True, port=int(sys.argv[1]))
    elif len(sys.argv) == 3 and sys.argv[2].isdigit():
        app.run(debug=True, host=sys.argv[1], port=int(sys.argv[2]))
    else:
        app.run(debug=True)
