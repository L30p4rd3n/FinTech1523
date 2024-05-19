import json

import requests
from flask import current_app
from flask_login import current_user

from app import bcreds, UG, app, Advise, db


def do():
    with app.app_context():
        user = UG.query.filter_by(uid=2).first() #TODO CHANGE THIS SHIT
        url = 'https://api.coze.com/open_api/v2/chat'

        msg = (f"сгенерируй мне 5 советов для улучшения финансового профиля, если у пользователя риск {user.risk}",
               f"при среднем 8, предвидение {user.foresight} при среднем 45, рвение {user.zeal} при среднем 65,",
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
        a = r.json()
        # print(a["messages"][0]["content"])
        b = a["messages"][0]["content"].split('\n')
        print(b)# 2, 4, 6, 8 10
        for i in range(2, 11, 2):
            adv = Advise(adv=b[i])
            db.session.add(adv)



        db.session.commit()
        current_app.logger.error("what am i")
        current_app.logger.warning(b)
    return b
do()