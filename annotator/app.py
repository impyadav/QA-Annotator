import json
import re
from datetime import datetime
from uuid import uuid4

import jsonify
from exportSquadJson import ExportJson
from flask import Flask, request, jsonify
from flask import render_template, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class annoatations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paraid = db.Column(db.String(100), nullable=False)
    doc_id = db.Column(db.String(100), nullable=False, )
    para_tit = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100))
    entrydate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<annoatations %r>' % self.content


class questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paraid = db.Column(db.String(100), nullable=False)
    ques_id = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<questions %r>' % self.question


class answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(100), nullable=False)
    answer_id = db.Column(db.String(100), nullable=False)
    answer_content = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<answers %r>' % self.answer_content


db.create_all()


def addParas_SQL(listPara, filename):
    doc_id = str(uuid4())

    msg = ""
    rows = annoatations.query.filter_by(doc_id=doc_id)
    if (rows.count() == 0):
        a = 0
        for lstpara in listPara:
            if len(lstpara.strip()) > 10:
                a = a + 1
                try:
                    unique_id = str(uuid4())
                    annot = annoatations(paraid=unique_id, doc_id=doc_id, content=lstpara, status='fresh')
                    db.session.add(annot)
                    db.session.commit()
                    msg = doc_id
                except:
                    msg = "error in insert operation"

    return msg


def preprocess_data(data):
    data = re.sub('\r\n', '\n', data, flags=re.I)
    data = re.sub('\n+', '\n', data, flags=re.I)
    data = data.replace('\n', '<newline>')
    data = re.sub(' +', ' ', data, flags=re.I)
    data = re.sub('\t+', '\t', data, flags=re.I)
    data = data.replace('<newline>$', '')
    # data = re.sub(data, '\t', ' ', flags= re.I)
    paras = data.split("<newline>")
    return paras


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/details', methods=['GET'])
def deatils():
    rows = db.session.query(annoatations.doc_id, func.count(annoatations.doc_id)).group_by(annoatations.doc_id).all()

    return render_template('details.html', rows=rows)


docid = ""

@app.route('/processing', methods=['POST'])
def index_post():
    isin = request.form['isin']
    allText = ""
    if isin == "upload":
        f1 = request.files['file1']
        allText = str(f1.read().decode('utf8'))
        fname = f1.filename
    else:
        allText = request.form['textarea_val']
        fname = str(uuid4())
    lstPara = preprocess_data(allText)
    msg = addParas_SQL(lstPara, fname)
    if not msg.__contains__("error"):
        global docid
        docid = msg.strip()
    rows = annoatations.query.filter_by(doc_id=docid).filter_by(status='fresh').paginate(per_page=1, page=1,
                                                                                         error_out=True)
    return render_template('preview.html', rows=rows)


@app.route('/preview/<int:page_num>')
@app.route('/preview/<int:page_num>/<paraid>')
def preview(page_num, paraid='Anonymous'):
    if not paraid == 'Anonymous':
        me = annoatations.query.filter_by(paraid=paraid).first()
        me.status = 'del'
        db.session.commit()
        try:
            rows = annoatations.query.filter_by(doc_id=docid).filter_by(status='fresh').paginate(per_page=1,
                                                                                                 page=page_num,
                                                                                                 error_out=True)
        except:
            rows = annoatations.query.filter_by(doc_id=docid).filter_by(status='fresh').paginate(per_page=1,
                                                                                                 page=page_num - 1,
                                                                                                 error_out=True)
    else:
        rows = annoatations.query.filter_by(doc_id=docid).filter_by(status='fresh').paginate(per_page=1, page=page_num,
                                                                                             error_out=True)
    return render_template('preview.html', allDataCount=100, rows=rows)


def addingAns(quesid,ans_text):
    try:
        ans_id = str(uuid4())
        ans = answers(question_id=quesid, answer_id=ans_id, answer_content=ans_text)
        db.session.add(ans)
        db.session.commit()
        return jsonify({"success": ans_id})
    except:
        return jsonify({"error": "Not added"})

@app.route('/exportAsJson', methods=["GET", "POST"])
def exportAsJson():
    # para_id = request.form['paraid']
    if request.method == "GET":
        classObj = ExportJson(r'db1.sqlite3', 'annoatations', 'questions', 'answers')
        with open('annotations.json', 'w') as outfile:
            json.dump(classObj.sql_df_to_squad_json(), outfile)
        try:
            return render_template("download.html")
        except Exception as e:
            return str(e)
        
        # try:
        #     return send_file(
        #             "annotations.json",
        #             as_attachment=True,
        #             attachment_filename="annotations.json"
        #         )
        # except Exception as e:
        #     return str(e)


@app.route('/download')
def download():
   return send_file('annotations.json', as_attachment=True)

@app.route('/annotThis', methods=["GET", "POST"])
def annotThis():
    if request.method == "POST":
        ques_id = str(uuid4())
        para_id = request.form['paraid']
        para_tit = request.form['para_tit']
        
        ques_text = request.form['question']
        ans_text = request.form['answer']
        try:
            db.session.query(annoatations).filter(annoatations.paraid == para_id).update({'para_tit': para_tit})
            db.session.commit()
            try:
                quest = questions(paraid=para_id, ques_id=ques_id, question=ques_text)
                db.session.add(quest)
                db.session.commit()
                anscount = ans_text.split('|')
                listAns = []
                for ans in anscount:
                    if ans != "":
                        listAns.append(ans)
                        ans_add = addingAns(ques_id, ans)
                return jsonify({"para_id": para_id, "ques_id": ques_id, "ques_text": ques_text,
                                    "ans_text": [ans + '<br/>' for ans in listAns]})
            except:
                return jsonify({"error": "Not added"})

        except Exception as ex:
            return jsonify({"error": "Not added"})


@app.route('/getQues', methods=["POST"])
def getQues():
    if request.method == "POST":
        para_id = request.form['paraid']
        try:
            quest = questions.query.filter_by(paraid=para_id).all()
            allQues = []
            for ques in quest:
                answerslst = answers.query.filter_by(question_id=ques.ques_id).all()
                anslst = []
                for ans in answerslst:
                    anslst.append(ans.answer_content)
                allQues.append(
                    dict(quesid=ques.ques_id, ques_txt=ques.question, ans_txt=[ans1 + '<br/>' for ans1 in anslst]))

            return jsonify(allQues)
        except:
            return "error"


@app.route('/delQues', methods=["POST"])
def delQues():
    if request.method == "POST":
        quesid = request.form['ques_id']
        try:
            me = questions.query.filter_by(ques_id=quesid).first()
            db.session.delete(me)
            db.session.commit()
            me = answers.query.filter_by(question_id=quesid).first()
            db.session.delete(me)
            db.session.commit()
            return "Record Deleted!"
        except:
            return "error"

@app.route('/delAnsTxtArea', methods=["POST"])
def delAnsTxtArea():
    if request.method == "POST":
        anstxtareaid = request.form['anstxtarea_id']
        try:
            me = questions.query.filter_by(answer_id=anstxtareaid).first()
            db.session.delete(me)
            db.session.commit()
            # me = answers.query.filter_by(quesid=anstxtareaid).first()
            # db.session.delete(me)
            # db.session.commit()
            return "Record Deleted!"
        except:
            return "error"


if __name__ == '__main__':
    db.create_all()
    # app.run(port=5004)
    app.run(use_debugger=True, use_reloader=False, passthrough_errors=True)
# serve(app, host='0.0.0.0', port=7765)
