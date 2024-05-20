import sqlite3

from flask import render_template, request, Blueprint, current_app, Response
from flask_login import current_user, login_required
import requests
import json

from app import db, UG, bcreds, Advise

game = Blueprint('game', __name__, url_prefix="/game")


@game.route('/')
@login_required
def load_vari():
    return render_template("game.html")


@game.route('/v', methods=["post"])
def vari():
    user = UG.query.filter_by(uid=current_user.id).first()
    zeal, foresight, risky = user.zeal, user.foresight, user.risk

    if user.day >= 31 or user.money < 0:
        current_user.new_user = 0
        db.session.commit()
        return "", 202

    else:
        if current_user.new_user == 1:
            current_user.new_user = 2
            db.session.commit()
        v = request.get_data()
        if v == b'1':
            if not user.worked:
                user.zeal += 1
                db.session.commit()
            return Response("/api/g/skip", mimetype="text/plain")
        elif v == b'2':
            return Response("/api/g/check", mimetype="text/plain")
        elif v == b'3':
            user.foresight += 1
            db.session.commit()
            return Response("/api/g/buy", mimetype="text/plain")
        elif v == b'4':
            return Response("/api/g/sell", mimetype="text/plain")
        elif v == b'5':
            return Response("/api/g/next", mimetype="text/plain")
        elif v == b'6':
            user.risk += 1
            db.session.commit()
            return Response("/api/g/rps", mimetype="text/plain")
        elif v == b'7':
            user.risk += 1
            db.session.commit()
            return Response("/api/g/poker", mimetype="text/plain")
        else:
            return "", 400


@game.route("/genadv", methods=["post"])
def generate():
    user = UG.query.filter_by(uid=current_user.id).first()
    advices = Advise.query.filter_by(uid=current_user.id).all()
    if advices == []:
        url = 'https://api.coze.com/open_api/v2/chat'

        msg = (f"сгенерируй мне 5 советов для улучшения финансового профиля, если у пользователя риск {user.risk}",
               f"при среднем 8, предвидение {user.foresight} при среднем 15, рвение {user.zeal} при среднем 12,",
               f"но не выводи показателей, так как они концидециальны")
        creds = bcreds.query.all()[0]
        headers = {
            'Authorization': f'{creds.cr1}',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'api.coze.com',
            'Connection': 'keep-alive'
        }
        data = {
            "conversation_id": "123",
            "bot_id": f"{creds.cr2}",
            "user": "123333333",
            "query": f"{msg}",
            "stream": False
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        current_app.logger.warning("got that JSON")
        a = r.json()
        b = a["messages"][0]["content"].split('\n')
        for i in range(len(b)):
            current_app.logger.warning(b)
            # if "1" == b[i][0] or "2" == b[i][0] or "3" == b[i][0] or "4" == b[i][0] or "5" == b[i][0]: # I CANT TAKE IT ANYMORE WHY DOESNT ANY WORK
            if "1." in b[i] or "2." in b[i] or "3." in b[i] or "4." in b[i] or "5." in b[i]:
                adv = Advise(adv=b[i], uid=current_user.id)
                db.session.add(adv)
                db.session.commit()
    return Response("generated advs", mimetype="text/plain"), 200