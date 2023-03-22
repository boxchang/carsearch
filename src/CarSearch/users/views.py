import datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from bases.views import index
from users.forms import CurrentCustomUserForm, CustomUser
from users.models import UserAuthority


@login_required
def user_auth(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')

        defaults = {
            'CARTYPE': False,
            'CARCOLOR': False,
            'CARAGE': False,
            'COMPANY': False,
            'COMPANY2': False,
            'DEBIT': False,
            'ENDDATE': False,
            'ACCNO': False,
            'GRADE': False,
            'COMPMAN': False,
            'CASENO': False,
            'VDATE': False,
            'FINDMODE': False,
            'CHGDATE': False,
            'CHGREC': False,
            'NOTE2': False,
            'MAN': False,
            'VID': False,
            'ADDR1': False,
            'ADDR2': False,
            'ADDR3': False,
            'ADDR4': False,
            'TEL1': False,
            'TEL2': False,
            'TEL3': False,
            'TEL4': False,
            'OTH1': False,
            'OTH2': False,
            'OTH3': False,
            'OTH4': False,
            'DOWNLOAD_CAR_LIST': False
        }

        if request.POST.get('CARTYPE'):
            defaults[''] = True
        if request.POST.get('CARCOLOR'):
            defaults[''] = True
        if request.POST.get('CARTYPE'):
            defaults['CARTYPE'] = True
        if request.POST.get('CARCOLOR'):
            defaults['CARCOLOR'] = True
        if request.POST.get('CARAGE'):
            defaults['CARAGE'] = True
        if request.POST.get('COMPANY'):
            defaults['COMPANY'] = True
        if request.POST.get('COMPANY2'):
            defaults['COMPANY2'] = True
        if request.POST.get('DEBIT'):
            defaults['DEBIT'] = True
        if request.POST.get('ENDDATE'):
            defaults['ENDDATE'] = True
        if request.POST.get('ACCNO'):
            defaults['ACCNO'] = True
        if request.POST.get('GRADE'):
            defaults['GRADE'] = True
        if request.POST.get('COMPMAN'):
            defaults['COMPMAN'] = True
        if request.POST.get('CASENO'):
            defaults['CASENO'] = True
        if request.POST.get('DATE'):
            defaults['DATE'] = True
        if request.POST.get('FINDMODE'):
            defaults['FINDMODE'] = True
        if request.POST.get('CHGDATE'):
            defaults['CHGDATE'] = True
        if request.POST.get('CHGREC'):
            defaults['CHGREC'] = True
        if request.POST.get('NOTE2'):
            defaults['NOTE2'] = True
        if request.POST.get('MAN'):
            defaults['MAN'] = True
        if request.POST.get('ID'):
            defaults['ID'] = True
        if request.POST.get('ADDR1'):
            defaults['ADDR1'] = True
        if request.POST.get('ADDR2'):
            defaults['ADDR2'] = True
        if request.POST.get('ADDR3'):
            defaults['ADDR3'] = True
        if request.POST.get('ADDR4'):
            defaults['ADDR4'] = True
        if request.POST.get('TEL1'):
            defaults['TEL1'] = True
        if request.POST.get('TEL2'):
            defaults['TEL2'] = True
        if request.POST.get('TEL3'):
            defaults['TEL3'] = True
        if request.POST.get('TEL4'):
            defaults['TEL4'] = True
        if request.POST.get('OTH1'):
            defaults['OTH1'] = True
        if request.POST.get('OTH2'):
            defaults['OTH2'] = True
        if request.POST.get('OTH3'):
            defaults['OTH3'] = True
        if request.POST.get('OTH4'):
            defaults['OTH4'] = True
        if request.POST.get('DOWNLOAD_CAR_LIST'):
            defaults['DOWNLOAD_CAR_LIST'] = True

        obj, created = UserAuthority.objects.update_or_create(pk=pk, defaults)

        if created:
            obj.create_by = request.user
        else:
            obj.update_by = request.user
        obj.save()

        return redirect('user_list')





@login_required
def create(request):
    template = 'users/create.html'
    if request.method == 'GET':
        form = CurrentCustomUserForm()
        form.fields['password1'].required = True
        form.fields['password2'].required = True

        return render(request, template, {'userForm': form})

    if request.method == 'POST':
        form = CurrentCustomUserForm(request.POST)
        form.fields['password1'].required = True
        form.fields['password2'].required = True
        if form.is_valid():
            user = form.save(commit=False)
            user.create_by = request.user
            user.update_by = request.user
            user.set_password(form.cleaned_data["password"])
            user.save()
            #messages.success(request, '歡迎註冊')
            return redirect('user_list')
        else:
            return render(request, template, {'userForm': form})


@login_required
def detail(request):
    template = 'users/edit.html'
    if request.method == 'POST':
        pk = request.POST.get('pk')
        member = CustomUser.objects.get(pk=pk)
        form = CurrentCustomUserForm(instance=member)
        return render(request, template, locals())

@login_required
def user_edit(request):
    template = 'users/edit.html'
    if request.method == 'POST':
        pk = request.POST.get('pk')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        member = CustomUser.objects.get(pk=pk)
        form = CurrentCustomUserForm(request.POST, instance=member)
        if form.is_valid():
            user = form.save(commit=False)
            user.create_by = request.user
            user.update_by = request.user
            if password1 and password2:
                user.set_password(password1)
            user.save()
            return redirect('user_list')
    return render(request, template, locals())

@login_required
def user_list(request):
    template = 'users/list.html'
    members = CustomUser.objects.all()
    for member in members:
        if member.is_active:
            member.is_active_text = "啟用"
            member.is_active_color = "bg-success"
        else:
            member.is_active_text = "停用"
            member.is_active_color = "bg-danger"

        if member.last_login:
            member.last_login_color = "bg-primary"
        else:
            member.last_login_color = "bg-secondary"

        yesterday = datetime.datetime.now() - datetime.timedelta(days=-1)
        if member.expired_date > yesterday:
            member.expired_date_color = "bg-danger"
        else:
            member.expired_date_color = "bg-success"

    return render(request, template, locals())


def login(request):
    if 'username' in request.COOKIES:
        cookies_username = request.COOKIES['username']

    if 'password' in request.COOKIES:
        cookies_password = request.COOKIES['password']

    '''
    Login an existing user
    '''
    template = 'users/login.html'
    if request.method == 'GET':
        next = request.GET.get('next')
        return render(request, template, locals())

    if request.method == 'POST':
        next_page = request.POST.get('next')
        if request.user.is_authenticated:
            if next_page != 'None':
                return HttpResponseRedirect(next_page)
            else:
                return index(request)
        else:
            # POST
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:    # Server-side validation
                messages.error(request, '使用者名稱或密碼未填寫！')
                return render(request, template)

            user = authenticate(username=username, password=password)
            if not user:    # authentication fails
                messages.error(request, '使用者名稱或密碼不正確！')
                return render(request, template)

            response = redirect(reverse('index'))
            if request.POST.get('remember') == "on":
                response.set_cookie("username", username, expires=timezone.now()+datetime.timedelta(days=30))
                response.set_cookie("password", password, expires=timezone.now()+datetime.timedelta(days=30))
            else:
                response.delete_cookie("username")
                response.delete_cookie("password")
            # login success
            auth_login(request, user)

            # messages.success(request, '登入成功')

            return response


def logout(request):
    '''
    Logout the user
    '''
    auth_logout(request)
    messages.success(request, '歡迎再度光臨')
    return redirect('login')
