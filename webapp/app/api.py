import tempfile
import json
import pandas as pd
import logging
from datetime import datetime

from classifier import classify

from flask import Flask, request, render_template, send_file, abort, send_from_directory, redirect

app = Flask(__name__)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    return redirect("/cli/form.html")

@app.route('/cli/<path:path>')
def send_cli(path):
    return send_from_directory('cli', path)

@app.route('/regulate', methods=['GET', 'POST'])
def regulate():
    if "spreadsheet" in request.files:
        return regulate_spreadsheet()
    else:
        return regulate_json()

def regulate_json():

    if request.method != 'POST':
        abort(400, "Faça requisição via POST")

    t = get_treshould()
    solicitacoes = request.form['solicitacoes']
    texts = json.loads(solicitacoes)
    
    # para garantir que ignora eventuais linhas em branco
    texts = [ x.strip() for x in texts if x.strip() != ""]

    preds = classify(texts, t)
    preds_df = pd.DataFrame.from_dict(preds)
    
    save_copy(texts, preds, t)

    response = app.response_class(
        status=200,
        response=preds_df.to_json(),
        mimetype='application/json'
    )

    return response


def get_treshould():
    str_t = request.args.get('t', '0.5')
    str_t = str_t.replace(",", ".")

    threshould = float(str_t)

    return threshould

def regulate_spreadsheet():

    if request.method != 'POST':
        # abort(400, "Faça requisição via POST")
        return show_form()

    if "spreadsheet" in request.files:
        f = request.files['spreadsheet']

        data_df = pd.read_excel(f)

        texts = data_df["QUADROCLINICO"].values

        t = get_treshould()
        preds = classify(texts, t)
        
        save_copy(texts, preds, t)
        
        data_df["_APROVADO"] = preds["pred_bin"]
        data_df["_PROBA_0"] = [ x[0] for x in preds["pred_probas"] ]
        data_df["_PROBA_1"] = [ x[1] for x in preds["pred_probas"] ]

        tf = tempfile.NamedTemporaryFile(suffix=".xlsx")
        data_df.to_excel(tf.name, index=False)

        attachment_filename = "regulada_%s" % f.filename
        return send_file(tf.name, as_attachment=True, attachment_filename=attachment_filename)


def save_copy(texts, preds, treshould):
    
    date_time_fname = datetime.now().strftime('%d%b%Y_%H%M%S')
    date_time = datetime.now().strftime('%d/%m/%Y %H:%M')

    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr    

    our_copy_fpath = "copias/%s.csv" % (date_time_fname)

    our_copy = {} 
    our_copy.update({"_PROBA_0": preds["pred_probas"][0]})
    our_copy.update({"_PROBA_1": preds["pred_probas"][1]})
    our_copy.update({"_APROVADO": preds["pred_bin"]})
    our_copy.update({"QUADROCLINICO": texts})

    our_copy_df = pd.DataFrame.from_dict(our_copy)
    our_copy_df["LIMIAR"] = treshould    
    our_copy_df["IP"] = user_ip
    our_copy_df["DATA HORA"] = date_time

    our_copy_df.to_csv(our_copy_fpath, sep=";", encoding="utf-8", index=False, header=True)
    logging.debug("Criado arquivo %s com cópia dos dados enviados por %s" % (our_copy_fpath, request.remote_addr))

if __name__ == "__main__":
    app.run()