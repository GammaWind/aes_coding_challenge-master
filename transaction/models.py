
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

from datetime import date



# Masters required in transaction models
class BranchMaster(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(blank=True, null=True, max_length=10)


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=20, unique=True)


class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gst_number = models.CharField(max_length=20, unique=True)
    supplier_status = models.BooleanField(default=False)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    remarks = models.CharField(max_length=200, blank=True)


class ArticleMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    blend_pct = models.CharField(max_length=50)
    twists = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True)


class ColorMaster(models.Model):
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    remarks = models.CharField(max_length=64, blank=True)

#generetor
def GenerateTransactionNumber():
    last = Transaction.objects.all().last()
    if not last:
        return 'TRN-' + '1-' + str(date.today().year)

    last_transaction = last.transaction_number
    

    spl = last_transaction.split('-')
    number = int(spl[1])
    number += 1
    
    year = spl[2]

    current_year = date.today().year

    if int(current_year) > int(year):
        return 'TRN-' + '1-' + str(current_year)
    else:
        return 'TRN-' + str(number) + '-' + str(current_year)   






# Create your models here.

class Transaction(models.Model):

    class TrnasStatus(models.TextChoices):
        PENDING = 'PENDING', 
        COMPLETED = 'COMPLETED', 
        CLOSE = 'CLOSE', 
        


    id = models.AutoField(unique=True,primary_key=True)

    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.CASCADE)
    branch = models.ForeignKey(BranchMaster, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    transaction_number = models.CharField(unique=True,db_index=True,default=GenerateTransactionNumber,max_length=100)
    transaction_status = models.CharField(max_length=10,choices=TrnasStatus.choices)
    remarks = models.CharField(blank=True, null=True, max_length=60)


class LineItem(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    transaction_number = models.ForeignKey(Transaction,to_field='transaction_number', db_column='transaction_number', on_delete=models.CASCADE,related_name='line_items')
    article = models.ForeignKey(ArticleMaster, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorMaster, on_delete=models.CASCADE)
    required_on_date = models.DateTimeField(blank=False);
    quantity = models.DecimalField(blank=False,decimal_places=2,max_digits=10)
    rate_per_unit = models.IntegerField(blank=False)

    class Units(models.TextChoices):
        KG = 'KG', 
        METER = 'METER', 

       

    unit = models.CharField(max_length=10,choices=Units.choices)

    class Meta:
        unique_together = (('transaction_number','article', 'color'))


class InventoryItem(models.Model):
    line_item = models.ForeignKey(LineItem, on_delete=CASCADE,related_name='inventory_items')
    article = models.ForeignKey(ArticleMaster, on_delete=CASCADE)
    color = models.ForeignKey(ColorMaster, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.CASCADE)
    gross_quantity = models.DecimalField(blank=False,decimal_places=2,max_digits=10)
    net_quantity = models.DecimalField(blank=False,decimal_places=2,max_digits=10)
    
    class Units(models.TextChoices):
        KG = 'KG', 
        METER = 'METER', 
       

    unit = models.CharField(max_length=10,choices=Units.choices)











