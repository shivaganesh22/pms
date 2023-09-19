from django.shortcuts import render,redirect
from app.forms import *
from django.db.models import Max
from django.forms import inlineformset_factory
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
@login_required
def home(r):
    id=r.user
    pl=id.placement_set.all()
    return render(r,"index.html",{'data':pl})
def signin(r):
    if r.method=='POST':
        username=r.POST['username']
        password=r.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(r,user)
            return redirect('home')
    return render(r,'signin.html')
@user_passes_test(lambda u:u.is_superuser)
def admi(r):
    return render(r,'admin/home.html')
def signout(r):
    logout(r)
    return redirect('home')
@user_passes_test(lambda u:u.is_superuser)
def addstudent(r):
    if r.method=='POST':
        name=r.POST['name']
        email=r.POST['email']
        username=r.POST['username']
        password=r.POST['password']
        if  User.objects.filter(username=username):
            messages.error(r,'Student already exists')
        else:
            User.objects.create_user(first_name=name,username=username,email=email,password=password)
            return redirect('admi')
    return render(r,'admin/addstudent.html')
@user_passes_test(lambda u:u.is_superuser)
def students(r):
    stud=User.objects.order_by('username')
    return render(r,'admin/students.html',{'students':stud})
@user_passes_test(lambda u:u.is_superuser)
def studedit(r,id):
    stud=User.objects.get(id=id)
    form=signup(instance=stud)
    if r.method=='POST':
        form=signup(r.POST,instance=stud)
        if form.is_valid():
            form.save()
            return redirect('students')
    return render(r,'admin/studedit.html',{'form':form})
@user_passes_test(lambda u:u.is_superuser)
def studdelete(r,id):
    stud=User.objects.get(id=id)
    stud.delete()
    return redirect('students')
@login_required
def changepassword(r):
    if r.method=='POST':
        p1=r.POST['p1']
        p2=r.POST['p2']
        if p1!=p2:
            messages.error(r,'Passwords doesnot match')
        else:
            r.user.set_password(p1)
            r.user.save()
            return redirect('home')
    return render(r,'changepassword.html')
@user_passes_test(lambda u:u.is_superuser)
def addcompany(r):
    form=Companyform()
    if r.method=='POST':
        form=Companyform(r.POST)
        if form.is_valid():
            form.save()
            return redirect('companies')
    return render(r,'admin/addcompany.html',{'form':form})
@user_passes_test(lambda u:u.is_superuser)
def companies(r):
    com=Companies.objects.order_by('annualpack')
    return render(r,'admin/companies.html',{'companies':com})
@user_passes_test(lambda u:u.is_superuser)
def comedit(r,id):
    com=Companies.objects.get(id=id)
    form=Companyform(instance=com)
    if r.method=='POST':
        form=Companyform(r.POST,instance=com)
        if form.is_valid():
            form.save()
            return redirect('companies')
    return render(r,'admin/comedit.html',{'form':form})
@user_passes_test(lambda u:u.is_superuser)
def comdelete(r,id):
    com=Companies.objects.get(id=id)
    com.delete()
    return redirect('companies')
@user_passes_test(lambda u:u.is_superuser)
def placements(r):
    com=Companies.objects.order_by('annualpack')
    return render(r,'admin/placements.html',{'companies':com})
@user_passes_test(lambda u:u.is_superuser)
def manage(r,id):
    form=inlineformset_factory(Companies,Placement,fields=('student',),can_delete=True,extra=3)
    s=Companies.objects.get(id=id)
    formset=form(queryset=Placement.objects.filter(company_id=id),instance=s)
    if r.method=="POST":
        formset=form(r.POST,instance=s)
        if formset.is_valid():
            formset.save()
            return redirect(f'/a/manage/{id}')
    return render(r,"admin/manage.html",{'form':formset})
@user_passes_test(lambda u:u.is_superuser)
def view(r,id):
    com=Companies.objects.get(id=id)
    stud=com.placement_set.all()
    return render(r,'admin/view.html',{'students':stud})
@login_required
def viewplace(r,id):
    com=Companies.objects.get(id=id)
    stud=com.placement_set.all()
    return render(r,'view.html',{'students':stud})
@login_required
def placement(r):
    com=Companies.objects.order_by('annualpack')
    return render(r,'placement.html',{'companies':com})
@login_required
def highlights(r):
    com=Placement.objects.order_by('company__annualpack').last()
    com=Placement.objects.filter(company__annualpack=com.company.annualpack)
    return render(r,'highlights.html',{'companies':com})
@user_passes_test(lambda u:u.is_superuser)
def ahighlights(r):
    com=Placement.objects.order_by('company__annualpack').last()
    com=Placement.objects.filter(company__annualpack=com.company.annualpack)
    return render(r,'admin/high.html',{'companies':com})
@user_passes_test(lambda u:u.is_superuser)
def sendnotification(r):
    if r.method=='POST':
        msg=r.POST['message']
        Notification(msg=msg).save() 
        return redirect('notifications')
    return render(r,'admin/sendnotification.html')
@user_passes_test(lambda u:u.is_superuser)
def managenotification(r):
    noti=Notification.objects.all()
    return render(r,'admin/managenotifications.html',{'i':noti})
@user_passes_test(lambda u:u.is_superuser)
def delnotification(r,id):
    noti=Notification.objects.get(id=id)
    noti.delete() 
    return redirect('notifications')
@login_required
def notifications(r):
    noti=Notification.objects.all()
    return render(r,'notifications.html',{'i':noti})