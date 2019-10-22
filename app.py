from flask import Flask, render_template, request
from main import Query

app = Flask(__name__)

query = Query()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/obtain_answer')
def obtain_answer():
    question = request.args.get('question')
    answer = query.query(question)
    return answer


if __name__ == '__main__':
    app.debug = True
    app.run()
