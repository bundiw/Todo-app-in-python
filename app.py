
import json
from os import abort
import sys
from urllib import response
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import Index

app = Flask(__name__)
db = SQLAlchemy(app)
Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=True)
    lid = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<ID {self.id} to-DO {self.tname}>'


class Todo_list(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(), nullable=False)
    selected = db.Column(db.Boolean(), default=False, nullable=True)
    todos = db.relationship('Todo', backref='todos.id')

    def __repr__(self):
        return f'<ID {self.id} to-DO {self.lname}>'


# db.create_all()
db.session.commit()


@app.route('/<lid>/complete_all', methods=['PATCH'])
def complete_all(lid):
    err = False
    try:
        complete_str = request.data
        complete = json.loads(complete_str)['selected']
        todo_list = Todo_list.query.filter_by(id=lid).first()
        todo_list.selected = complete
        all_todo = Todo.query.filter_by(lid=lid).all()
        for todo in all_todo:
            todo.completed = complete
        db.session.commit()

    except:
        err = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if err:
            abort()
        else:
            return redirect(url_for('index'))


@app.route('/<tid>/set-completed', methods=['PATCH'])
def check_item(tid):
    body = {}
    err = False

    try:
        data_str = request.data
        data_dic = json.loads(data_str)
        todo = Todo.query.get(tid)
        item = Todo.query.filter_by(id=tid).first().tname
        body['tname'] = item

        todo.completed = data_dic['completed']

        db.session.commit()

    except:
        db.session.rollback()
        err = False
        print(sys.exc_info())

    finally:
        db.session.close()
        if err:
            abort()

        else:
            return jsonify(body)
            # render_template('index.html', data=res)


@app.route('/<list_id>/delete-category')
def delete_category(list_id):
    err = False

    try:
        all_todo_under_category = Todo.query.filter_by(lid=list_id).delete()
        # print("first", all_todo_under_category)
        # print("second", list_id)

        Todo_list.query.filter_by(id=list_id).delete()
        db.session.commit()

    except:
        db.session.rollback()
        err = True
        print(sys.exc_info())

    finally:
        db.session.close()
        if err:
            abort()
        else:
            return jsonify({response: all_todo_under_category})


@app.route('/<lid>/create_todo', methods=['POST'])
def create(lid):
    data_str = request.data
    data_dic = json.loads(data_str)
    error = False

    # {"tname": "uik", "lid": "1"}
    try:

        itm = Todo(tname=data_dic['tname'], lid=lid)

        db.session.add(itm)

        db.session.commit()
        # db.session.expunge_all()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:

        if not error:
            # body = Todo.query.order_by('id').all()

            db.session.close()
            # print(body)
            return redirect(url_for('index'))
        else:
            abort()


@app.route('/<id>/item-delete/')
def delete_item(id):

    err = False

    try:
        # print("two: ", todoid)
        todo = Todo.query.get(id)
        # Todo.query.filter_by(id=todo).delete()
        db.session.delete(todo)
        db.session.commit()

    except:
        db.session.rollack()
        err = True
        print(sys.exc_info())

    finally:
        db.session.close()
        if err:
            abort()
        else:
            return redirect(url_for('index'))


@app.route('/<lid>/todos')
def show_todo(lid):
    # print(lid)
    dat = {}
    err = False

    try:
        dat = Todo.query.filter_by(lid=lid).order_by('id').all()
        # =[{'tname': 'c2'}, ]
        # print(dat)
        lists = Todo_list.query.order_by('id').all()

    except:
        err = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if err:
            abort()
        else:
            return render_template('index.html', data=dat, lists=lists, lid=lid)


@app.route('/add-list', methods=['POST'])
def create_list():
    err = False
    new_list_str = request.data
    try:
        new_list = json.loads(new_list_str)
        new_category = Todo_list(lname=new_list['lname'])
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        err = True
    finally:
        db.session.close()
        if err:
            abort()
        else:
            return new_list_str


@app.route('/', methods=['GET', 'POST', 'PATCH'])
def index():
    err = False
    try:
        lists = Todo_list.query.order_by('id').all()
        # print(dat)
        dat = Todo.query.filter_by(lid=1).order_by('id').all()
        db.session.commit()

    except:
        err = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        if err:
            abort()
        else:
            return render_template('index.html',  data=dat, lists=lists)


if __name__ == "__main__":

    app.run(host="0.0.0.0")
    app.run(debug=True)
