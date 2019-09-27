from movie.models import BasedOnId, BasedOnTitle
from rest_framework import serializers

class BasedOnIdSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BasedOnId
        fields = "__all__"


class BasedOnTitleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BasedOnTitle
        fields = "__all__"
