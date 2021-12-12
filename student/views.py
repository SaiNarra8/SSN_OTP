from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import openpyxl
from quiz.models import Passage,Email,LongPassage


def exam_section2_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/section2.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response

    
    
def passage_view(request):
      if "GET" == request.method:
        return render(request, 'quiz/passage.html', {})
      else:
        excel_file1 = request.FILES["excel_file"]    

        # you may put validations here to check extension or file size

        wb1 = openpyxl.load_workbook(excel_file1)

        # getting a particular sheet by name out of many sheets
        worksheet = wb1["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        print(excel_data)
        count = 0
        for i in excel_data:
            if count == 0:
               count = count + 1
               continue
    
            p=Passage.objects.create(passage_qs=i[0])
            q=LongPassage.objects.create(longpassage_qs=i[1])
            r=Email.objects.create(email_qs=i[2])
            

            
            p.save()
            q.save()
            r.save()

           
            
            
            



               
           

        return render(request, 'quiz/passage.html', {"excel_data":excel_data})
#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)
    



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    passages=Passage.objects.all()
    emails=Email.objects.all()
    paginator = Paginator(questions, 1)
    page = request.GET.get('page')
    paged_questions = paginator.get_page(page)
    longpassages=LongPassage.objects.all()
    if pk == 2:
           response= render(request,'student/start_exam.html',{'course':course,'questions':questions,'passages':passages})
    if pk == 3:
           response= render(request,'student/start_exam.html',{'course':course,'questions':questions,'longpassages':longpassages})
    if pk == 4:
           response= render(request,'student/start_exam.html',{'course':course,'questions':questions,'emails':emails})


    if request.method=='POST':
        pass
    if pk == 1:

        response= render(request,'student/start_exam.html',{'course':course,'questions':paged_questions})
    response.set_cookie('course_id',course.id)
    return response

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def dummy_view(request):
  
    questions=QMODEL.Question.objects.all()
    if request.method=='POST':
        pass
    response= render(request,'student/dummy.html',{'questions':questions})
   
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all()
        k=0
        for q in questions:
            selected_ans = request.COOKIES.get(str(k+1))
            k = k + 1
            actual_answer = q.answer 
            if selected_ans == actual_answer:
                total_marks = total_marks + q.marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})
  