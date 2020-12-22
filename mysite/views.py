from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import *
from django.db.models import Sum, Value as V, F
from django.db.models.functions import Coalesce
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
    if request.method == 'POSTs':
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
            group_in = mmd.UserToGroup.objects. \
                filter(linked_user__django_user_id=user_id). \
                values_list("linked_group")
        except mmd.UserToGroup.DoesNotExist:
            return render(request, "db-page-diff-list-n.html",
                          {'diff': None, 'warning': warning, 'w_type': w_type})
        all_group_people = mmd.UserProfile.objects.none()
        for g in group_in:
            try:
                all_group_people |= mmd.UserToGroup.objects.filter(linked_group=g).values_list("linked_user")
            except mmd.UserToGroup.DoesNotExist:
                continue
        all_diff = mmd.Compare.objects.values_list("id", "upd1__info", "upd2__info", "create_date", "info").none()
        for p in all_group_people:
            try:
                all_diff |= mmd.Compare.objects.filter(create_user=p). \
                    values_list("id", "upd1__info", "upd2__info", "create_date", "info")
            except mmd.Compare.DoesNotExist:
                continue
        all_diff_short = []
        for info in all_diff:
            str_u1 = info[1]
            str_u2 = info[2]
            str_in = info[4]
            if len(str_u1) > 20:
                str_u1 = str_u1[:20] + '...'
            if len(str_u2) > 20:
                str_u1 = str_u2[:20] + '...'
            if len(str_in) > 20:
                str_u1 = str_in[:20] + '...'
            all_diff_short.append((info[0], str_u1, str_u2, info[3], str_in))
        if len(all_diff_short) == 0:
            all_diff_short = None
        return render(request, "db-page-diff-list-n.html",
                      {'diff': all_diff_short, 'warning': warning, 'w_type': w_type})
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
        group_info_short = []
        for info in group_list:
            if len(info[2]) > 30:
                tmp = (info[0], info[1], info[2][:30] + '...')
                group_info_short.append(tmp)
            else:
                group_info_short.append(info)
        if len(group_info_short) == 0:
            group_info_short = None
        info_get = {'group_list': group_info_short, 'warning': warning, 'w_type': w_type}
        return render(request, "db-page-group-list.html", info_get)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


def group(request, group_id):
    # TODO: link to group page
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


# Experiment part
def list_exps(request, warning=None, w_type=0):
    if request.user.is_authenticated:
        user_id = request.user.id
        try:
            groups_in = mmd.UserToGroup.objects.filter(linked_user__django_user_id=user_id). \
                values_list("linked_group")
        except mmd.UserToGroup.DoesNotExist:
            return render(request, "db-page-exps-list.html", {'exp_list': None, 'warning': warning, 'w_type': w_type})
        exp_list = mmd.ExpToGroup.objects. \
            values_list("linked_exp__id", "linked_group__name", "linked_exp__info", "linked_exp__create_date").none()
        for g in groups_in:
            try:
                exp_list |= mmd.ExpToGroup.objects.filter(linked_group=g). \
                    values_list("linked_exp__id", "linked_group__name", "linked_exp__info", "linked_exp__create_date")
            except mmd.ExpToGroup.DoesNotExist:
                continue
        exp_list_short = []
        for exp in exp_list:
            if len(exp[2]) > 40:
                exp_list_short.append((exp[0], exp[1], exp[2][:40] + '...', exp[3]))
            else:
                exp_list_short.append(exp)
        if len(exp_list_short) == 0:
            exp_list_short = None
        return render(request, "db-page-exps-list.html",
                      {'exp_list': exp_list_short, 'warning': warning, 'w_type': w_type})
    else:
        return redirect(login_page, info='Please Login', i_type=1)


def delete_exps(request, exp_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        try:
            the_exp = mmd.Experiment.objects.get(id=exp_id)
        except mmd.Experiment.DoesNotExist:
            return redirect(list_exps, warning='Invalid Experiment ID', w_type=0)
        if the_exp.create_user.django_user_id == user_id:
            the_exp.delete()
            return redirect(list_exps, warning='Delete Successfully', w_type=1)
        try:
            owned_group = mmd.ExpToGroup.objects.get(linked_exp=the_exp)
        except mmd.ExpToGroup.DoesNotExist:
            return redirect(list_exps, warning='You Do Not Have The Permission To Delete', w_type=0)
        if owned_group.linked_group.owner.django_user_id == user_id:
            the_exp.delete()
            return redirect(list_exps, warning='Delete Successfully', w_type=1)
        return redirect(list_exps, warning='You Do Not Have The Permission To Delete', w_type=0)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


# Message part
def get_all_message(user):
    try:
        issues_out = mmd.Issue.objects.filter(create_user__django_user_id=user.id).order_by('create_date')
        new_issues_out = issues_out.count(status=1)
    except mmd.Issue.DoesNotExist:
        issues_out = None
        new_issues_out = 0
    try:
        applies_out = mmd.Apply.objects.filter(create_user__django_user_id=user.id).order_by('create_date')
        new_applies_out = applies_out.count(status=1)
    except mmd.Apply.DoesNotExist:
        applies_out = None
        new_applies_out = 0
    try:
        all_update = mmd.Update.objects.filter(create_user__django_user_id=user.id)
        issues_in = mmd.Issue.objects.none()
        for upd in all_update:
            try:
                issues_in |= mmd.Issue.objects.filter(target_update=upd)
            except mmd.Issue.DoesNotExist:
                continue
        issues_in = issues_in.order_by('create_date')
        new_issues_in = issues_in.count(status=0)
    except mmd.Update.DoesNotExist:
        issues_in = None
        new_issues_in = 0
    try:
        all_group = mmd.Group.objects.filter(owner__django_user_id=user.id)
        applies_in = mmd.Apply.objects.none()
        for gro in all_group:
            try:
                applies_in |= mmd.Apply.objects.filter(target_group=gro)
            except mmd.Apply.DoesNotExist:
                continue
        applies_in = applies_in.order_by('create_date')
        new_applies_in = applies_in.count(status=0)
    except mmd.Group.DoesNotExist:
        applies_in = None
        new_applies_in = 0
    return {'ap_in': applies_in,
            'n_ap_in': new_applies_in,
            'is_in': issues_in,
            'n_is_in': new_issues_in,
            'ap_out': applies_out,
            'n_ap_out': new_applies_out,
            'is_out': issues_out,
            'n_is_out': new_issues_out}


def list_message(request, warning=None, w_type=0):
    if request.user.is_authenticated:
        all_message = get_all_message(request.user)
        all_message['warning'] = warning
        all_message['w_type'] = w_type
        return render(request, "db-page-message.html", all_message)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


def answer_apply(request, app_id, ans_type):
    if request.user.is_authenticated:
        try:
            the_app = mmd.Apply.objects.get(id=app_id)
        except mmd.Apply.DoesNotExist:
            return redirect(list_message, warning="Something Wrong.", w_type=0)
        if the_app.target_group__owner__django_user_id == request.user.id:
            if ans_type == 1:   # accept
                new_link = mmd.UserToGroup(
                    linked_user=the_app.create_user, linked_group=the_app.target_group)
                new_link.save()
                the_app.status = 1
                the_app.reply = True
                the_app.save()
            else:               # refused
                the_app.status = 1
                the_app.reply = False
                the_app.save()
            return redirect(list_message, warning='Succeed.', w_type=1)
        else:
            return redirect(list_message, warning='Do not have permission.', w_type=0)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


def answer_issue(request, iss_id):
    if request.user.is_authenticated:
        try:
            the_iss = mmd.Issue.objects.get(id=iss_id)
        except mmd.Issue.DoesNotExist:
            return redirect(list_message, warning="Something Wrong.", w_type=0)
        if the_iss.target_update__create_user__django_user_id == request.user.id:
            answer = request.POST['input_answer']
            the_iss.status = 1
            the_iss.answer_info = answer
            the_iss.save()
            return redirect(list_message, warning='Succeed.', w_type=1)
        else:
            return redirect(list_message, warning='Do not have permission.', w_type=0)
    else:
        return redirect(login_page, info='Please Login', i_type=1)


def mark_read_app(request, app_id):
    if request.user.is_authenticated:
        try:
            the_app = mmd.Apply.objects.get(id=app_id)
        except mmd.Apply.DoesNotExist:
            return redirect(list_message, warning="Something Wrong.", w_type=0)
        pass
    else:
        return redirect(login_page, info='Please Login', i_type=1)


# Error
def page_not_found(request, exception):
    return render(request, "page-404.html")

def exp(request):
    # if not request.user.is_authenticated:
    #     return render(request, "page-login.html")
    # user_id = request.user.id
    user_id = 1

    try:
        current_user = User.objects.filter(id=user_id).values_list("username")[0][0]
        current_user_info, img_current_user = UserProfile.objects. \
            filter(django_user_id=user_id). \
            values_list("info", "avatar")[0]

    except User.DoesNotExist:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        current_user = 0
        current_user_info = 0
        img_current_user = 0

    # comments = [{
    #     "avatar": i.avatar,
    #     "commenter_name": i.commenter_name,
    #     "commenter_info": i.commenter_info,
    #     "info": i.info,
    #     "create_date": i.create_date,
    # } for i in comments]

    print(f"get exp {request.GET.get('exp')}")
    my_exp = Experiment.objects.filter(name=request.GET.get("exp", "")).annotate(
        builder=F('create_user_id__django_user_id__username'),
        img_builder=F('create_user_id__avatar'),
    )[0]

    link = 'linked_upd_id__'
    my_upds = UpdToExp.objects.filter(linked_exp_id=my_exp.id).annotate(
        name=F(link + 'name'),
        updater=F(link + 'create_user_id__django_user_id__username'),
        img_updater=F(link + 'create_user_id__avatar'),
        update_time=F(link + 'create_date'),
        update_intro=F(link + 'info'),
        imgs=F(link + 'imgs')
    )

    my_upd = request.GET.get("upd", None)
    if my_upd:
        my_upd = my_upds.filter(name=my_upd)[0]
    else:
        my_upd = my_upds[0]

    exp_upds = [my_upd.name] + [i[0] for i in my_upds.values_list("name") if i[0] != my_upd.name]

    comments = Comment.objects.annotate(
        avatar=F('create_user_id__avatar'),
        commenter_name=F('create_user_id__django_user_id__username'),
        commenter_info=F('create_user_id__info'),
        # info
        # create_date
    ).filter(target_update_id=my_upd.id)

    upd_imgs = my_upd.imgs.split(',')

    # print(my_upd.update_time)
    dict_diff = {
        # page2
        "diffs": [0],
        "diff1": 0,
        "diff2": 0,
        "img_diff_updater": 0,
        "diff_time": 0,
        "diff_updater": 0,
        "intro1": 0,
        "intro2": 0,
        "diff_imgs": [],
        "diff_title": 0,
        "diff_intro": 0,
        "num_diff_comments": 0,
        "comment_diff": [],  # er, er_img

    }

    return render(request, "db-page-exp.html", {
        "img_exp_builder": my_exp.img_builder,
        "exp_name": my_exp.name,
        "exp_builder": my_exp.builder,
        "exp_intro": my_exp.info,
        "exp_updates": exp_upds,

        "img_updater": my_upd.img_updater,
        "updater": my_upd.updater,
        "update_time": my_upd.update_time,
        "update_name": my_upd.name,
        "update_intro": my_upd.update_intro,
        "img_update": upd_imgs,
        "num_comment": len(comments),

        "comments": comments,

        "current_user": current_user,
        "img_current_user": img_current_user,
        "current_user_info": current_user_info,

        **dict_diff
    })


def cmt_upd(request):
    # if not request.user.is_authenticated:
    #     return render(request, "page-login.html")
    # user_id = request.user.id
    user_id = 1

    print(request.POST, "!!!!!!!")
    # print(request.headers, request.body)

    # new_cmt = Comment(create_user=user_id, target_update=0, info=0)

    referer = request.headers.get("Referer", None)
    if referer:
        return redirect(referer)
    else:
        return JsonResponse({"status": 200, "message": "add cmt of upd succeed"})
