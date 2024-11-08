from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BookDetails(models.Model):
    name=models.CharField(max_length=128)
    book_code=models.IntegerField()
    author_name=models.CharField(max_length=128)
    date=models.DateField()
    status=models.CharField(max_length=128)
    amount=models.IntegerField()
    available_books = models.IntegerField()
    created_date=models.DateField()
    created_by=models.IntegerField()
    updated_date=models.DateField(null=True)
    updated_by=models.IntegerField(null=True)
    book_img = models.FileField(upload_to='image')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "book_details"

# Create your models here.
class StudentDetails(models.Model):
    username=models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    wallet_balance = models.FloatField(default = 5000)
    status=models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'student_details'



#2 entry
#1st entry - auth user
#2nd entry - student_table


class Booktransferhistory(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    code=models.IntegerField()
    book_name=models.CharField(max_length=128)
    status = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add=True)

    
class UserBookDetails(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    books_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserBookStatus(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    book = models.ForeignKey(BookDetails,on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
