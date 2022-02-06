from django.db import models
from enquiry.models import Enquiry
from django.contrib.auth.models import User 
from PIL import Image
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.timezone import timedelta
from ckeditor.fields import RichTextField
# from users.models import Employee
# Create your models here.

class Quotation(models.Model):
    enquiry = models.ForeignKey(Enquiry,on_delete=models.CASCADE)
    date_posted=models.DateTimeField(default=timezone.now)
    price_quotated = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    attachment = models.FileField(upload_to='quotation_attachments',default = 'default.jpg',null = True)
    # person = models.ForeignKey(Employee,on_delete=models.DO_NOTHING,default = 1)

    def delete(self,*args,**kwargs):   # delete the attachment of the attachment if the enquiry is deleted 
        self.attachment.delete()
        super().delete(*args,**kwargs)
    def save(self, *args, **kwargs): # delete the attachment if the new attachment has been added
        self.total_price = self.price_quotated * self.enquiry.qty
        try:
            this = Enquiry.objects.filter(id=self.id)
            if this.attachment != self.attachment:
                this.attachment.delete()
        except: pass
        super(Quotation, self).save(*args, **kwargs)
    def __str__(self):
        return f'enqid {self.enquiry.id}'
