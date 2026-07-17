from django.shortcuts import render,get_object_or_404,redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import URL
from .serializers import URLSerializer
from .utils import encode_base62
from django.utils import timezone


# Create your views here.



@api_view(["POST"])                                 #this is an api end point view function that recives POST request from the user (the url)
def create_short_url(request):
    serializer = URLSerializer(data=request.data)   #the request contains url only so the sreializer direclty takes the data and uses it(check in serializers.py)

    if not serializer.is_valid():                    #check if the serializer is a valid URL or not
     return Response(serializer.errors,status=400)   #if not valid then return sattus code 400

    original_url=serializer.validated_data["original_url"]

    qs=URL.objects.filter(original_url=original_url)
   
    url=qs.first()

    base_url=request.build_absolute_uri("/")[:-1]       #retrives the base url

    if url is None:

      url=URL(original_url=original_url)       
      url.save()                              #save the url to the URL modle | 'url' is the object for that

      url.short_code=encode_base62(url.id)    #get the id created by the db for the saved url and encode it by base62 function defined in utils.py and assign it to the short_code field of the db
      url.save()                              #save the changes in db
                                              #the id is a defult db field that incerements itself for each entry
   
    return Response({
         
         "short_code":url.short_code,
         "short_url":f"{base_url}/{url.short_code}"       #return the short code and the formatted short url to the user
                        
                        
                        })
   




@api_view(["GET"])                          #This is a get request end point
def redirect_url(request,short_code):       #short_code variable is intialized at urls.py
  
   url=get_object_or_404(URL,short_code=short_code)     #retrive the url from the URL table of db where short_code is the one initialized at urls.py
                                                        #we can retrive the short_code from the request by request.path(will return smthg like--> /GB) but django does this and sends as argument from the urls.py for us
   
   url.click_count+=1;              #increment the click count
   url.last_accessed=timezone.now() #update the last accessed time
   url.save()


   return redirect(url.original_url)    #instead of rendering a html or responding a json we redirect the user to the origianl link
                                        #here there is no json from the user end we use the endpoint(short_code to take actions)


@api_view(["GET"])                                    #this is a GET end point to send the analyzed data for each stored url
def url_stats(request,short_code):                    #simply get the data of the requested shortcode then respond with the data
   url=get_object_or_404(URL,short_code=short_code)

   return Response({
      "click_count" : url.click_count,
      "last_accessed" : url.last_accessed,
      "created_at" : url.created_at
   })