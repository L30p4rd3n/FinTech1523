import flask
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from app import db, User, Advise, Stocks, SU
from flask_login import login_required, current_user, logout_user, login_user
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

api = Blueprint('api', __name__, url_prefix='/api')
r = Blueprint('r', __name__, url_prefix='/r')
api.register_blueprint(r)


@r.route('/game', methods=["PATCH"])
def game_response():
    if current_user.is_anonymous:
        return abort(403)
    data = request.get_json()
    response = {}
    if list(data.keys())[0] == "risk":
        response["status_code"] = "200"
        current_user.is_risky = int(data["risk"])
        current_user.invest = int(data["invest"])
        current_user.new_user = 0
        db.session.commit()
    else:
        response["status_code"] = "204"
    return flask.jsonify(response)


@api.route('/test1', methods=["GET"])
def give_stock():
    # if current_user.is_anonymous:
    #    return abort(404)  # stylise 404 and 403 into one error template.
    # else:
    response = {"code": 200,
                "body":
                    {

                    }
                }
    for i in range(1, 50):
        a = Stocks.query.filter_by(id=i).first()
        response["body"][f"opt{i}"] = {"name": a.fname,
                                       "code": a.boardid}
    return flask.jsonify(response)


@api.route('/test11', methods=["PATCH"])
def update_us_db():
    data = request.get_json()
    request_data = list(data["body"].keys())
    selected = SU.query.filter_by(uid=current_user.id).all()
    all_selected_IDs = []
    user_before_IDS = [selected[i].sid for i in range(len(selected))]
    for i in range(len(request_data)):
        name = Stocks.query.filter_by(boardid=request_data[i]).first()
        all_selected_IDs.append(name.id)
    for i in range(len(user_before_IDS)):
        if user_before_IDS[i] not in all_selected_IDs:
            con = sqlite3.connect("/instance/hella_db.sqlite")
            cur = con.cursor()
            take = cur.execute(f"SELECT all FROM SU WHERE uid='{current_user.id}' AND sid='{user_before_IDS[i]}'")
            delete = cur.execute(f"DELETE FROM su WHERE uid='{current_user.id}' AND sid='{user_before_IDS[i]}'")
    for i in range(len(all_selected_IDs)):
        if all_selected_IDs[i] not in user_before_IDS:
            insert = SU(uid=current_user.id, sid=all_selected_IDs[i])
            db.session.add(insert)
            db.session.commit()

    # all_stock_IDs = [list_of_stocks[i].id for i in range(len(list_of_stocks))]

    response = {"code": {
        "answer": 200
    },
        "body":
            {
                "res": f"{request_data}"
            }
    }
    return flask.jsonify(response)


@api.route("/tests", methods=["GET", "PUT", "POST", "DELETE", "PATCH"])
def tests_page():
    return render_template("test.html")


# def tests():
#    data = request.get_json()
#    if len(data):
#        pass


@api.route('/passwd_change', methods=["PATCH"])
def change():
    passwds = request.get_json()
    old_pass = passwds["old"]
    new_pass = passwds["new"]
    if check_password_hash(current_user.password, old_pass):
        current_user.password = generate_password_hash(new_pass, method='sha256')
        db.session.commit()
        logout_user()

        # Сделать окно перехода через секунду???

        return flask.jsonify({"response": 200})
    else:
        return flask.jsonify({"response": 304})


@api.route("/login", methods=["POST"])
def check_passwd():
    udata = request.get_json()
    login = udata["login"]
    password = udata["password"]
    remember = udata["remember"]
    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password, password):
        abort(401)
    # login code goes here
    login_user(user, remember=remember)
    return {}

@api.route("/delete_user", methods=["DELETE"])
def delete_user():
    who = User.query.filter_by(id=current_user.id).first()
    db.session.delete(who)
    db.session.commit()
    return flask.jsonify({"response": 204})
