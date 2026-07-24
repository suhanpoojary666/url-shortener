from django.shortcuts import render,get_object_or_404,redirect

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import URL
from .serializers import *
from .utils import encode_base62
from django.utils import timezone
from django.contrib.auth.models import User


# Create your views here.

@api_view(["POST"])                                 #this is an api end point view function that recives POST request from the user (the url)
@permission_classes([IsAuthenticated])
def create_short_url(request):
    serializer = URLSerializer(data=request.data)   #the request contains url only so the sreializer direclty takes the data and uses it(check in serializers.py)

    if not serializer.is_valid():                    #check if the serializer is a valid URL or not
     return Response(serializer.errors,status=400)   #if not valid then return sattus code 400

    original_url=serializer.validated_data["original_url"]
    
    custom_alias=serializer.validated_data.get("custom_alias")  #ailas if sent None if not sent by the user

    qs=URL.objects.filter(original_url=original_url,owner=request.user)  #returns query set <[url:Gb]> or <[]>
   
    url=qs.first()                                    #retruns object [url:Gb] or None

    base_url=request.build_absolute_uri("/")[:-1]     #retrives the base url

    if url is None:                                   #if url is None create one else direclty retrun the retrived one\

      if custom_alias:                                #if the custom_alias was passed use it as short code

         chck=URL.objects.filter(short_code=custom_alias).first()      #get the object where the shortcode is the alias given

         if chck:                                     #if the object is already present respond with an error message
            return Response({
               "error":f"The custom alias {custom_alias} already exists"
            })
         
         url=URL(original_url=original_url)       #save the url to the URL modle | 'url' is the object for that
      
         url.short_code=custom_alias              #save the alias as the short code
         url.owner = request.user
         url.save()

      else:

         url=URL(original_url=original_url,owner=request.user)       
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



@api_view(["POST"])
def register(request):
   serializer=RegisterSerializer(data=request.data)
   
   if not serializer.is_valid():
      return Response(serializer.errors,status=400)         #validate the response
   
   username=serializer.validated_data["username"]           #retrive the data from the validated response
   password=serializer.validated_data["password"]

   existing_user=User.objects.filter(username=username).first()    #check if the username already exists

   if existing_user:
      return Response({
         "error":"username already exist's"
      })

   user=User.objects.create_user(username=username,password=password) #Way of creating User model(class) object "user" where password is hashed automatically part of the built in user model of django

   #Success response
   return Response(
    {
        "message": "User registered successfully."
    },
    status=201
)

@api_view(["GET"])
@permission_classes([IsAuthenticated]) #requires authentication
def my_urls(request):
   urls=URL.objects.filter(owner=request.user)  

   serializer=URLResponseSerializer(urls,many=True)

   return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_url(request,short_code):

   url=get_object_or_404(URL,short_code=short_code)               #URL does not exists then return 404 else retrive the object

   if url.owner != request.user:

      return Response({
         "error" : "You are not authorized to delete this URL"    #URL does not belong to the user
      },status=403,)
   
   url.delete()                                                   #After all the checks delete the URL from db

   return Response({
      "messege":"URL deleted successfully"
   })

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_url(request,short_code):

    base_url = request.build_absolute_uri("/")[:-1]         #build the base url for response

    url=get_object_or_404(URL,short_code=short_code)        #retrive the object from the db with corresponding short_code

    if request.user!=url.owner:                             #check if the user owns the url

       return Response({
          "error":"You are not authorized to update this URL"
       },status=403,)

    serializer=UpdateSerializer(data=request.data)          #validate the custom_alias sent by the user(JSON->py. object)

    if not serializer.is_valid():                           
       return Response(serializer.errors,status=400)

    new_code=serializer.validated_data["custom_alias"]      #retrive the new short code

    existing_url=URL.objects.filter(short_code=new_code).first()  #check if the custom_alias is already used

    if existing_url:
       
       if existing_url != url:                                 
         return Response({
            "error": "Custom alias already exists."
         },status=400,)
       
       else:
        return Response({                                      #If the custom_alias is same as short_code of the same url just return dont access the db
             "message": "Alias updated successfully.",
             "short_url": f"{base_url}/{url.short_code}",
           })

    url.short_code=new_code
    url.save()
    
    return Response({
      "message": "Alias updated successfully.",
      "short_url": f"{base_url}/{url.short_code}",
    })
