# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class BankCard(models.Model):
    uuid = models.AutoField("唯一标识", primary_key=True)
    owner_id = models.CharField("用户id", max_length=16, default="")
    image = models.ImageField(upload_to='bankcards', max_length=255)
    card_num = models.CharField("卡号码", max_length=32, null=True, blank=True)
    bank = models.CharField("所属银行", max_length=32, null=True, blank=True)
    card_type = models.IntegerField("类型", null=True, blank=True)
    create_at = models.DateTimeField("上传时间", default=datetime.now)

    def __str__(self):
        return str(self.uuid) + self.card_num


class IdCard(models.Model):
    uuid = models.AutoField("唯一标识", primary_key=True)
    owner_id = models.CharField("用户id", max_length=16, default="")
    image = models.ImageField(upload_to='idcards', max_length=255)
    id_num = models.CharField("身份证号码", max_length=32, null=True, blank=True)
    id_name = models.CharField("姓名", max_length=32, null=True, blank=True)
    gender = models.CharField("性别", max_length=8, null=True, blank=True)
    address = models.CharField("地址", max_length=64, null=True, blank=True)
    nation = models.CharField("民族", max_length=8, null=True, blank=True)
    create_at = models.DateTimeField("上传时间", default=datetime.now)

    def __str__(self):
        return str(self.uuid) + self.id_name + self.id_num


