from rest_framework import serializers


class URLSerializer(serializers.Serializer):
    original_url = serializers.URLField()  #only urls are accepted as api imputs form the user(else 400-error)
                                           #The the URL recived at the views.py API endpoint is intialized to this variable