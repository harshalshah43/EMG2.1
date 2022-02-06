from django.db import models
from django.db import models
from django.contrib.auth.models import User 
from PIL import Image
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.timezone import timedelta

# from ems2.quotation.models import Quotation

phone_regex=RegexValidator(regex=r'^\ ?1?\d{9,15}$',message="Phone no must be entered in format: Up to 10 digits allowed.")

class Enquiry(models.Model):
    # attachment = models.FileField(upload_to='enquiry_attachments',default = 'default.jpg',null = True)
    date_posted=models.DateField(default=timezone.now)
    party = models.CharField(max_length=50)
    brand_choices = [('abb','ABB'),('legrand','LEGRAND'),('phoenix mecano','PHEONIX MECANO'),('eaton','EATON'),('Bussmann','Bussmann')]
    brand = models.CharField(choices = brand_choices,max_length = 40,default="Bussmann")
    item_code = models.CharField(max_length=50,default='')
    qty =models.IntegerField(default=0)
    status_choices = [('Open','Open'),('Quoted','Quoted'),('Converted','Converted'),('Failed','Failed')]
    status = models.CharField(choices = status_choices,max_length =10,default = 'Open',null=True)
    cust_type_choices = [('OEM','OEM'),('Ex','Ex'),('T','T'),('En','En'),('C','C'),('A','A')]
    cust_type = models.CharField(max_length=10,choices=cust_type_choices,default='T')
    media_choices = [('E','E'),('W','W'),('A','A')]
    media = models.CharField(max_length=10,choices=media_choices,default = 'E')
    
    def delete(self,*args,**kwargs):   # delete the attachment of the attachment if the enquiry is deleted 
        self.attachment.delete()
        super().delete(*args,**kwargs)
    def save(self, *args, **kwargs): # delete the attachment if the new attachment has been added
        try:
            this = Enquiry.objects.filter(id=self.id)
            if this.attachment != self.attachment:
                this.attachment.delete()
        except: pass
        super(Enquiry, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.id} {self.party}'


class Contact(models.Model):
    enquiry = models.ForeignKey(Enquiry,on_delete=models.CASCADE)
    phone=models.CharField(validators=[phone_regex],max_length=10,default=None,null=True)
    email = models.EmailField(default = 'null@noemail.com')
    address = models.CharField(max_length = 150, default = 'No address')