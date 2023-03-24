import datetime

from django.contrib.auth.models import Permission
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
from django.http import JsonResponse


def add_permission(user, codename):
    codename = 'view_' + str(codename).lower()
    perm = Permission.objects.get(codename=codename)
    user.user_permissions.add(perm)

def remove_permission(user, codename):
    codename = 'view_' + str(codename).lower()
    perm = Permission.objects.get(codename=codename)
    user.user_permissions.remove(perm)


# Ajax API
@login_required
def user_auth_api(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')

        user = CustomUser.objects.get(pk=pk)

        if request.POST.get('CARTYPE'):
            add_permission(user, 'CARTYPE')
        else:
            remove_permission(user, 'CARTYPE')

        if request.POST.get('CARCOLOR'):
            add_permission(user, 'CARCOLOR')
        else:
            remove_permission(user, 'CARCOLOR')

        if request.POST.get('CARAGE'):
            add_permission(user, 'CARAGE')
        else:
            remove_permission(user, 'CARAGE')

        if request.POST.get('COMPANY'):
            add_permission(user, 'COMPANY')
        else:
            remove_permission(user, 'COMPANY')

        if request.POST.get('COMPANY2'):
            add_permission(user, 'COMPANY2')
        else:
            remove_permission(user, 'COMPANY2')

        if request.POST.get('DEBIT'):
            add_permission(user, 'DEBIT')
        else:
            remove_permission(user, 'DEBIT')

        if request.POST.get('ENDDATE'):
            add_permission(user, 'ENDDATE')
        else:
            remove_permission(user, 'ENDDATE')

        if request.POST.get('ACCNO'):
            add_permission(user, 'ACCNO')
        else:
            remove_permission(user, 'ACCNO')

        if request.POST.get('GRADE'):
            add_permission(user, 'GRADE')
        else:
            remove_permission(user, 'GRADE')

        if request.POST.get('COMPMAN'):
            add_permission(user, 'COMPMAN')
        else:
            remove_permission(user, 'COMPMAN')

        if request.POST.get('CASENO'):
            add_permission(user, 'CASENO')
        else:
            remove_permission(user, 'CASENO')

        if request.POST.get('VDATE'):
            add_permission(user, 'VDATE')
        else:
            remove_permission(user, 'VDATE')

        if request.POST.get('FINDMODE'):
            add_permission(user, 'FINDMODE')
        else:
            remove_permission(user, 'FINDMODE')

        if request.POST.get('CHGDATE'):
            add_permission(user, 'CHGDATE')
        else:
            remove_permission(user, 'CHGDATE')

        if request.POST.get('CHGREC'):
            add_permission(user, 'CHGREC')
        else:
            remove_permission(user, 'CHGREC')

        if request.POST.get('NOTE2'):
            add_permission(user, 'NOTE2')
        else:
            remove_permission(user, 'NOTE2')

        if request.POST.get('MAN'):
            add_permission(user, 'MAN')
        else:
            remove_permission(user, 'MAN')

        if request.POST.get('VID'):
            add_permission(user, 'VID')
        else:
            remove_permission(user, 'VID')

        if request.POST.get('ADDR1'):
            add_permission(user, 'ADDR1')
        else:
            remove_permission(user, 'ADDR1')

        if request.POST.get('ADDR2'):
            add_permission(user, 'ADDR2')
        else:
            remove_permission(user, 'ADDR2')

        if request.POST.get('ADDR3'):
            add_permission(user, 'ADDR3')
        else:
            remove_permission(user, 'ADDR3')

        if request.POST.get('ADDR4'):
            add_permission(user, 'ADDR4')
        else:
            remove_permission(user, 'ADDR4')

        if request.POST.get('TEL1'):
            add_permission(user, 'TEL1')
        else:
            remove_permission(user, 'TEL1')

        if request.POST.get('TEL2'):
            add_permission(user, 'TEL2')
        else:
            remove_permission(user, 'TEL2')

        if request.POST.get('TEL3'):
            add_permission(user, 'TEL3')
        else:
            remove_permission(user, 'TEL3')

        if request.POST.get('TEL4'):
            add_permission(user, 'TEL4')
        else:
            remove_permission(user, 'TEL4')

        if request.POST.get('OTH1'):
            add_permission(user, 'OTH1')
        else:
            remove_permission(user, 'OTH1')

        if request.POST.get('OTH2'):
            add_permission(user, 'OTH2')
        else:
            remove_permission(user, 'OTH2')

        if request.POST.get('OTH3'):
            add_permission(user, 'OTH3')
        else:
            remove_permission(user, 'OTH3')

        if request.POST.get('OTH4'):
            add_permission(user, 'OTH4')
        else:
            remove_permission(user, 'OTH4')

        if request.POST.get('DOWNLOAD_CAR_LIST'):
            add_permission(user, 'DOWNLOAD_CAR_LIST')
        else:
            remove_permission(user, 'DOWNLOAD_CAR_LIST')

        msg = "權限更新完成"
        return JsonResponse(msg, safe=False)

# Create
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
        view_cartype = member.has_perm('users.view_cartype')
        view_carcolor = member.has_perm('users.view_carcolor')
        view_carage = member.has_perm('users.view_carage')
        view_company = member.has_perm('users.view_company')
        view_company2 = member.has_perm('users.view_company2')
        view_debit = member.has_perm('users.view_debit')
        view_enddate = member.has_perm('users.view_enddate')
        view_accno = member.has_perm('users.view_accno')
        view_grade = member.has_perm('users.view_grade')
        view_compman = member.has_perm('users.view_compman')
        view_caseno = member.has_perm('users.view_caseno')
        view_cdate = member.has_perm('users.view_cdate')
        view_findmode = member.has_perm('users.view_findmode')
        view_chgdate = member.has_perm('users.view_chgdate')
        view_chgrec = member.has_perm('users.view_chgrec')
        view_note2 = member.has_perm('users.view_note2')
        view_man = member.has_perm('users.view_man')
        view_cid = member.has_perm('users.view_cid')
        view_addr1 = member.has_perm('users.view_addr1')
        view_addr2 = member.has_perm('users.view_addr2')
        view_addr3 = member.has_perm('users.view_addr3')
        view_addr4 = member.has_perm('users.view_addr4')
        view_tel1 = member.has_perm('users.view_tel1')
        view_tel2 = member.has_perm('users.view_tel2')
        view_tel3 = member.has_perm('users.view_tel3')
        view_tel4 = member.has_perm('users.view_tel4')
        view_oth1 = member.has_perm('users.view_oth1')
        view_oth2 = member.has_perm('users.view_oth2')
        view_oth3 = member.has_perm('users.view_oth3')
        view_oth4 = member.has_perm('users.view_oth4')
        view_download_car_list = member.has_perm('users.view_download_car_list')

        form = CurrentCustomUserForm(instance=member)
        return render(request, template, locals())

# Edit
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
