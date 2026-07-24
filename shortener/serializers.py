from rest_framework import serializers


class URLSerializer(serializers.Serializer):    #recives data from the client (JSON----->python_object)
    original_url = serializers.URLField()  #only urls are accepted as api imputs form the user(else 400-error)
                                           #The the URL recived at the views.py API endpoint is intialized to this variable
    custom_alias = serializers.CharField(required=False)    #Validate the custom alias if sent else ignore



class RegisterSerializer(serializers.Serializer):       #this serializer validates the user regi. data sent by the cilent
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)     #only write dont send this in the response(protection layer-->write_only=True)



class URLResponseSerializer(serializers.Serializer):    #this is a response serializer (python_object--->JSON) used to send data to client from server
    original_url = serializers.URLField()
    short_code = serializers.CharField()
    click_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    last_accessed = serializers.DateTimeField(allow_null=True)

class UpdateSerializer(serializers.Serializer):
    custom_alias=serializers.CharField()