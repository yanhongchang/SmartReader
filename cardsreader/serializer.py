from rest_framework import serializers

from cardsreader.models import BankCard, IdCard


class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = ("owner_id", "image", "card_num", "bank", "card_type", "create_at")


class IdCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = IdCard
        fields = ("owner_id", "image", "id_num", "id_name", "gender",
                  "address", "nation", "create_at")
