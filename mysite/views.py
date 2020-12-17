from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

import mysite.models as mmd
import random


# Main page
def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return redirect(login_page, info='Please Login', i_type=1)


# Login part
def login_page(request, info=None, i_type=0):
    return render(request, "page-login.html", {'info': info, 'i_type': i_type})


def register_page(request, info=None, i_type=0):
    return render(request, "page-register.html", {'info': info, 'i_type': i_type})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        try:
            password = request.POST['signin-password']
            username = request.POST['signin-name']
        except MultiValueDictKeyError:
            return redirect(login_page, info='Invalid Username or Password', i_type=0)
        the_user = authenticate(username=username, password=password)
        if the_user is not None:
            login(request, the_user)
            return redirect(index)
        else:
            return redirect(login_page, info='Invalid Username or Password', i_type=0)
    return redirect(login_page, info='Something Wrong', i_type=0)


def sign_out(request):
    logout(request)
    return redirect(login_page, info='Log Out Successfully', i_type=1)


def get_random_avatar():
    i = random.randint(1, 4)
    if i == 1:
        return mmd.UserProfile.AvatarType.A
    elif i == 2:
        return mmd.UserProfile.AvatarType.B
    elif i == 3:
        return mmd.UserProfile.AvatarType.C
    else:
        return mmd.UserProfile.AvatarType.D


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        try:
            name = request.POST['username']
            password = request.POST['password']
            re_password = request.POST['re_password']
            info = request.POST['info']
            email = request.POST['email']
        except MultiValueDictKeyError:
            return redirect(register_page, info='Something Wrong', i_type=0)
        if re_password != password:
            return redirect(register_page, info='Incomparable Password', i_type=0)
        if User.objects.filter(username=name):
            return redirect(register_page, info='User exist, Please Change Your Name', i_type=0)
        new_user = User.objects.create_user(username=name, password=password, email=email)
        new_user.save()
        a = get_random_avatar()
        new_my_user = mmd.UserProfile(django_user=new_user, info=info, avatar=a)
        new_my_user.save()
        return redirect(login_page, info='Register Successfully, please sign in', i_type=1)
    else:
        return redirect(register_page, info='Something Wrong', i_type=0)


# Comparison part
def list_diff(request, warning=None, w_type=0):
    if request.user.is_authenticated:
        user_id = request.user.id
        try:
            group_in = mmd.UserToGroup.objects.\
                filter(linked_user__django_user_id=user_id).\
                values_list("linked_group")
        except mmd.UserToGroup.DoesNotExist:
            return render(request, "db-page-diff-list-n.html",
                          {'diff': None, 'warning': warning, 'w_type': w_type})
        all_group_people = mmd.UserProfile.objects.none()
        for g in group_in:
            try:
                all_group_people |= mmd.UserToGroup.objects.filter(linked_group=g)
            except mmd.UserToGroup.DoesNotExist:
                continue
        all_diff = mmd.Compare.objects.values_list("id", "upd1__info", "upd2__info", "create_date", "info").none()
        for p in all_group_people:
            try:
                all_diff |= mmd.Compare.objects.filter(create_user=p).\
                    values_list("id", "upd1__info", "upd2__info", "create_date", "info")
            except mmd.Compare.DoesNotExist:
                continue
        return render(request, "db-page-diff-list-n.html",
                      {'diff': all_diff, 'warning': warning, 'w_type': w_type})
    else:
        return redirect(login_page, info='Please Login', i_type=1)


def delete_diff(request, diff_id):
    if request.user.is_authenticated:
        try:
            diff_info = mmd.Compare.objects.get(id=diff_id)
        except mmd.Compare.DoesNotExist:
            return redirect(list_diff, warning='Comparison Does not Exist', w_type=0)
        if diff_info.create_user.django_user_id != request.user.id:
            return redirect(list_diff, warning='You Do Not Have The Permission To Delete', w_type=0)
        else:
            diff_info.delete()
            return redirect(list_diff, warning='Successfully Deleted', w_type=1)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


# Group part
def list_group(request, warning=None, w_type=0):
    if request.user.is_authenticated:
        try:
            people_id = request.user.id
            group_list = mmd.UserToGroup.objects. \
                filter(linked_user__django_user_id=people_id). \
                values_list("linked_group__id", "linked_group__name", "linked_group__info")
        except mmd.UserToGroup.DoesNotExist:
            group_list = None
        info_get = {'group_list': group_list, 'warning': warning, 'w_type': w_type}
        return render(request, "db-page-group-list.html", info_get)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


def group(request, group_id):
    return render(request, "db-page-group.html")


def create_group(request):
    if request.user.is_authenticated:
        master_user = mmd.UserProfile.objects.get(django_user_id=request.user.id)
        try:
            g_name = request.POST['name']
            g_info = request.POST['info']
        except KeyError:
            return redirect(list_group, warning='Invalid Name Or Info', w_type=0)
        new_group = mmd.Group(name=g_name, info=g_info, owner=master_user)
        try:
            new_group.save()
        except ValueError:
            return redirect(list_group, warning='Unable To Create Group', w_type=0)
        new_user_to_group = mmd.UserToGroup(linked_group=new_group, linked_user=master_user)
        try:
            new_user_to_group.save()
        except ValueError:
            return redirect(list_group, warning='Unable To Link Group And People', w_type=0)
        return redirect(list_group, warning='Created Successfully', w_type=1)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


# Error
def page_not_found(request, exception):
    return render(request, "page-404.html")
