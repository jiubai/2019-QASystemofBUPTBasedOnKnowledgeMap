from flask import Flask, render_template, request, jsonify
from query_question import Query
from redis_db import get_data_from_db_by_name, generate_html_by_data

from redis_db import update_history_question, update_common_question
from redis_db import get_history_question, get_common__question
from redis_db import update_QA_db
app = Flask(__name__)
update_QA_db()
query = Query()
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/obtain_answer')
def obtain_answer():

    question = request.args.get('question')
    answer = query.query(question)
    all_data = get_data_from_db_by_name(name=answer)
    answer = generate_html_by_data(all_data)
    print(answer)
    update_history_question(question)
    update_common_question(question)
    return answer


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000,debug=True)
    app.debug = True
    app.run()
