from django.db import models

from student.models import Student
class Course(models.Model):
   course_name = models.CharField(max_length=50,default=True)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.course_name

class Passage(models.Model):
    passage_qs=models.CharField(max_length=3000000)
 
class Email(models.Model):
    email_qs=models.CharField(max_length=3000000)
    
class LongPassage(models.Model):
    longpassage_qs=models.CharField(max_length=3000000)
    


  

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,default=True)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=2000)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    is_passage = models.BooleanField(default=False)
    is_longpassage = models.BooleanField(default=False)
    is_email=models.BooleanField(default=False)

    
    
  


    mp3file=models.FileField(default=True)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)



