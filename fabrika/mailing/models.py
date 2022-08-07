from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

class Mail(models.Model):
    pub_date = models.DateTimeField('date published')
    message_text = models.CharField(max_length=200)
    code_filter = models.CharField(max_length=200,blank=True,default="")
    tag_filter = models.CharField(max_length=200,blank=True,default="")
    end_time = models.DateTimeField('end date')
    owner = models.ForeignKey('auth.User', related_name='mails', on_delete=models.CASCADE,blank=True)

    def __str__(self) -> str:
        return f"{self.pub_date} - {self.end_time} - {self.message_text[0:10]}"

class Client(models.Model):
    phone = models.IntegerField(validators=[MaxValueValidator(79999999999), MinValueValidator(70000000000)])
    code = models.IntegerField()
    tag = models.CharField(max_length=200,blank=True,default="")
    timezone = models.IntegerField()

    def __str__(self):
        return f"{self.phone} - {self.tag} - {self.code}"

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

    def __str__(self) -> str:
        return f"{self.send_date} - {self.status}"




