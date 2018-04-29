import sendgrid
from App import app

sg = sendgrid.SendGridAPIClient(apikey=app.config["SENDGRID_APIKEY"])


def _send(users, subject, content):
    resp = sg.client.mail.send.post(request_body={
        "personalizations": [
            {
                "to": [
                    {"email": u.email, "name": u.username} for u in users
                ],
                "subject": subject
            }
        ],
        "from": {
            "name": "Kulukorvauslomake",
            "email": "noreply@fyysikkokilta.fi"
        },
        "content": [
            {
                "type": "text/html",
                "value": content
            }
        ]
    })
    return resp.status_code


def send_password_restore(user):
    url = "https://kulu.fyysikkokilta.fi/restore/{id}".format(id=user.restore_id)
    return _send([user], "Salasanan vaihto", """
        Hei,

        Olet ilmeisesti unohtanut salasanasi käyttäjälle {name},
        joten tässä sinulle palautuslinkki:

        <a href="{url}" target="_blank">{url}</a>

        Terveisin,
        Kulukorvauslomake
    """.format(url=url, name=user.username))


def send_bill_notification(users):
    url = "https://kulu.fyysikkokilta.fi/bills"
    return _send(users, "Uusia kulukorvauksia", """
        Hei,

        Killalle on tullut uusia kulukorvauspyyntöjä.
        Käy katsomassa pyynnöt <a href="{url}" target="_blank">täältä.</a>

        Terveisin,
        Kulukorvauslomake
    """.format(url=url))
