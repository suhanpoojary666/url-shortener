from django.db import models

# Create your models here.

class URL(models.Model):
    #basics
    original_url=models.URLField()                          #stores the original url
    short_code=models.CharField(max_length=10,unique=True)  #stores the short_code for the corresponding url
    created_at=models.DateTimeField(auto_now_add=True)      #stores the time of creation

    #click-analytics
    click_count=models.PositiveIntegerField(default=0)       #number of times a link was clicked
    last_accessed=models.DateTimeField(null=True,blank=True)    #time the link was last clicked

    def __str__(self):
        return self.short_code