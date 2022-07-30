from django.db import models


class Mail(models.Model):
    pub_date = models.DateTimeField('date published')
    message_text = models.CharField(max_length=200)
    code_filter = models.CharField(max_length=200,blank=True,default="")
    tag_filter = models.CharField(max_length=200,blank=True,default="")
    end_time = models.DateTimeField('end date')
    owner = models.ForeignKey('auth.User', related_name='mails', on_delete=models.CASCADE,blank=True)

class Client(models.Model):
    phone = models.IntegerField()
    code = models.IntegerField()
    tag = models.CharField(max_length=200,blank=True,default="")
    timezone = models.IntegerField()

MESSAGE_STATUS_CHOICES = [
    ('S', 'SEND'),
    ('A', 'AWAITING'),
    ('F', 'FAILED')
]
class Message(models.Model):
    send_date = models.DateTimeField('date send')
    status = models.CharField(max_length=1,choices=MESSAGE_STATUS_CHOICES,default='A')
    related_mail = models.ForeignKey(Mail,models.CASCADE)
    client = models.ForeignKey(Client,models.CASCADE)




