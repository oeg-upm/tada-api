from tada_hdt_entity.entity import EntityAnn
from tada_hdt_entity.parser import Parser
from tada_hdt_entity.entity import deref_list_string

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flasgger import swag_from, Swagger

import os

app = Flask(__name__)

UPLOAD_DIR = 'upload'
HDT_DIR = 'dbpedia.hdt'


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/subject', methods=['POST'])
@swag_from('subject.yml',validation=False)
def annotate_subject_col():
    col_id = int(request.form['col_id'])
    source_file = request.files['source']
    if 'alpha' in request.form:
        alpha = float(request.form['alpha'])
    else:
        alpha = 0.9
    if 'dbpedia_only' in request.form:
        dbpedia_only = bool(request.form['dbpedia_only'])
    else:
        dbpedia_only = True
    uploaded_dir = save_file(source_file)
    if uploaded_dir:
        ea = EntityAnn(HDT_DIR, "entity.log", alpha)
        ea.set_language_tag("@en")
        ea.set_title_case(True)
        parser = Parser(uploaded_dir)
        data = parser.parse_vertical()
        entities_ptr = ea.annotate_column(data, col_id, True, True)
        entities_all = [str(e) for e in entities_ptr]
        entities = []
        thing = 'http://www.w3.org/2002/07/owl#Thing'
        if dbpedia_only:
            for e in entities_all:
                if e.startswith('http://dbpedia.org/ontology/'):
                    entities.append(e)
                elif e==thing:
                    entities.append(thing)
        else:
            entities = entities_all
        # if thing not in entities:
        #     print("append owl:Thing")
        #     entities.append(thing)

        j = {
            "entities": entities,
        }
        # for e in entities:
        #     print e
        return jsonify(j)
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


swagger = Swagger(app)

if __name__ == '__main__':
    app.run(debug=True)