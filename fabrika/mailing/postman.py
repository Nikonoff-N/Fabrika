from .models import *
from django_rq import job
from datetime import datetime
import logging
import requests
import pytz
from requests.auth import HTTPBasicAuth
import json 
from django_rq.queues import get_queue
utc = pytz.UTC
logger = logging.getLogger("postman")

# defining the api-endpoint
API_ENDPOINT = "https://probe.fbrq.cloud/v1/send/"

# your API key here
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA2MjUyNjYsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkRTTmlrb25vZmYifQ.JzCjXYf44aDSmKcLHEXXt0FTmxbh58J9ydu2ivJ2oB0"

AUTH = HTTPBasicAuth('apikey', API_KEY)

HEADERS = {"Authorization": f"Bearer {API_KEY}"} 

def editMailing(mail:Mail):
    tochange = mail.message_set.filter(status='A')
    for m in tochange:
        m.status = 'F'
    addMailing(mail)


def addMailing(mail: Mail):
    clients = Client.objects.all()
    now = utc.localize(datetime.now())
    logger.info(f"{now} - got mails")
    if mail.code_filter:
        clients = clients.filter(code=mail.code_filter)
    if mail.tag_filter:
        clients = clients.filter(tag=mail.tag_filter)
    if mail.pub_date < now < mail.end_time:
        logger.info(f"{now} - look at time need to go!")
        for c in clients:
            logger.info(f"{now} - going to enque this {c}")
            sendMail.delay(c,mail)
    elif now > mail.end_time:
        logger.error(f"{now} - sad we too late")
    elif now < mail.pub_date:
        logger.info(f"{now} - will pub soon")
        for c in clients:
            scheduleMessege(c,mail)

@job
def sendMail(client: Client, mail: Mail):
    """
        creates message and sends it immedeately !
    """
    now = datetime.now()
    message = Message(send_date=now, status="A", related_mail=mail, client=client)
    message.save()
    sendMessege(message)


    # logger.info(f"{now} - {client}")
    # data = {
    #     "id": message.pk,
    #     "phone": client.phone,
    #     "text": mail.message_text,
    # }
    # json_object = json.dumps(data) 
    # #req = requests.Request(url=API_ENDPOINT + str(message.pk), json=json_object ,headers=HEADERS)
    # #prepared = req.prepare()
    # # pretty_log_POST(prepared)
    # #logger.info(str(prepared.headers) + str(prepared.body))
    # r = requests.post(url=API_ENDPOINT + str(message.pk), data=json_object ,headers=HEADERS)
    # if r.status_code == 200:
    #     message.status = "S"
    #     message.save()
    #     logger.info(f"{now} - send success")
    # else:
    #     message.status = "F"
    #     message.save()
    #     logger.info(f"{now} - failed with response:\n{r.status_code}\n{r.text}\n{r.url}")


def scheduleMessege(client: Client, mail: Mail):
    """
        creates message and schedules it to send
    """
    now = datetime.now()
    message = Message(send_date=mail.pub_date, status="A", related_mail=mail, client=client)
    message.save()
    logger.info(f"{now} - scheduling to send messege to {client} at {mail.pub_date}")
    queue = get_queue('default')
    job = queue.enqueue_at(mail.pub_date, sendMessege,message)


def sendMessege(messege:Message):
    """
    sends messege immedeatly
    """
    now = datetime.now()
    if messege.status == "A":
        data = {
        "id": messege.pk,
        "phone": messege.client.phone,
        "text": messege.related_mail.message_text,
        }
        json_object = json.dumps(data)
        r = requests.post(url=API_ENDPOINT + str(messege.pk), data=json_object ,headers=HEADERS)
        if r.status_code == 200:
            messege.status = "S"
            messege.save()
            logger.info(f"{now} - send success")
        else:
            messege.status = "F"
            messege.save()
            logger.info(f"{now} - failed with response:\n{r.status_code}\n{r.text}\n{r.url}")
    else:
        logger.info(f"{now} - messege was already send")


def sendMailAtTime(client: Client, mail: Mail):
    now = datetime.now()
    message = Message(send_date=now, status="A", related_mail=mail, client=client)
    message.save()
    logger.info(f"{now} - {client}")
    data = {
        "id": message.pk,
        "phone": client.phone,
        "text": mail.message_text,
    }
    json_object = json.dumps(data) 
    req = requests.Request(url=API_ENDPOINT + str(message.pk), json=json_object ,headers=HEADERS)
    prepared = req.prepare()
    # pretty_log_POST(prepared)
    logger.info(str(prepared.headers) + str(prepared.body))
    r = requests.post(url=API_ENDPOINT + str(message.pk), data=json_object ,headers=HEADERS)
    if r.status_code == 200:
        message.status = "S"
        message.save()
        logger.info(f"{now} - send success")
    else:
        message.status = "F"
        message.save()
        logger.info(f"{now} - failed with response:\n{r.status_code}\n{r.text}\n{r.url}")


# def pretty_log_POST(req):
#     """
#     At this point it is completely built and ready
#     to be fired; it is "prepared".

#     However pay attention at the formatting used in 
#     this function because it is programmed to be pretty 
#     printed and may differ from the actual request.
#     """
#     logger.info('{}\n{}\r\n{}\r\n\r\n{}'.format(
#         '-----------START-----------',
#         req.method + ' ' + req.url,
#         '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
#         req.body,
#     ))