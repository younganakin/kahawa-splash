from rest_framework import serializers
from .models import Radcheck


class RadcheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radcheck
        fields = ('username', 'attribute', 'op', 'value')
