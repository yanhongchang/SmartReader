# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

from cardsreader.serializer import BankCardSerializer, IdCardSerializer
from aip import AipOcr

baidu_client = AipOcr(settings.APP_ID, settings.API_KEY, settings.SECRET_KEY)

from django.http import HttpResponse

from .models import BankCard
def getvwamre(request):
    BankCard.objects.get_queryset()


def get_img_content(image_path):
    with open(image_path, 'rb') as fp:
        return fp.read()


class BankCard(APIView):

    def post(self, request, format=None):
        bankcardserial = BankCardSerializer(data=request.data)
        if bankcardserial.is_valid():
            bankcard_inst = bankcardserial.save()
            card_content = self.read_cardnum(bankcardserial)
            print(type(card_content))

            if 'error_code'not in card_content.keys():
                # update idcard to save card's msg
                result_dict = {
                    "card_num": card_content['result']['bank_card_number'],
                    "bank": card_content['result']['bank_name'],
                    "card_type": card_content['result']['bank_card_type']
                }
                bankcardserial.update(bankcard_inst, validated_data=result_dict)
                return Response(result_dict, status=status.HTTP_201_CREATED)
            else:
                return Response(card_content, status=status.HTTP_400_BAD_REQUEST)
        return Response(bankcardserial.errors, status=status.HTTP_400_BAD_REQUEST)

    def read_cardnum(self, cardserial):
        image_path = os.path.join(settings.MEDIA_ROOT, cardserial.data['image'])
        return baidu_client.bankcard(get_img_content(image_path))


class IdCard(APIView):

    def post(self, request, format=None):
        idcardserial = IdCardSerializer(data=request.data)
        if idcardserial.is_valid():
            idcard_instance = idcardserial.save()
            card_content = self.read_cardnum(idcardserial)

            # update idcard to save card's msg
            card_result = card_content['words_result']
            print(card_result)
            if len(card_result['公民身份号码']['words'])>0:

                result_dict = {
                    "id_num": card_result['公民身份号码']['words'],
                    "id_name": card_result['姓名']['words'],
                    "gender": card_result['性别']['words'],
                    "address": card_result['住址']['words'],
                    "nation": card_result['民族']['words']
                }
                idcardserial.update(idcard_instance, validated_data=result_dict)
                return Response(result_dict, status=status.HTTP_201_CREATED)
            else:
                card_content = {
                    "err_msg": "recognize ID card error,please try again..."
                }
                return Response(card_content, status=status.HTTP_400_BAD_REQUEST)
        return Response(idcardserial.errors, status=status.HTTP_400_BAD_REQUEST)

    def read_cardnum(self, cardserial):
        image_path = os.path.join(settings.MEDIA_ROOT, cardserial.data['image'])
        return baidu_client.idcard(get_img_content(image_path), "front")

