from flask import render_template, request, Blueprint
from flask_login import current_user

from app import db, UG

game = Blueprint('game', __name__, url_prefix="/game")


@game.route('/')
def load_vari():
    return render_template("game.html")


@game.route('/', methods=["get", "post"])
def vari():
    user = UG.query.filter_by(uid=current_user.id).first()
    zeal, foresight, risky = user.zeal, user.foresight, user.risk

    if user.day > 31 or user.money <= 0:
        if current_user.new_user != 0:
            current_user.new_user = 0
            # advices()
            db.session.commit()
        return "Game Over", 202
    else:
        v = request.get_data()
        if v == b'1':
            if not user.worked:
                user.zeal += 1
                db.session.commit()
            return "/api/game/skip"
        elif v == b'2':
            return "/api/game/check"
        elif v == b'3':
            foresight += 1
            return "/api/game/buy"
        elif v == b'4':
            return "/api/game/sell"
        elif v == b'5':
            return "/api/game/next"
        elif v == b'6':
            risky += 1
            return "/api/game/rps"
        elif v == b'7':
            risky += 1
            return "/api/game/poker"
        else:
            return " ", 400
