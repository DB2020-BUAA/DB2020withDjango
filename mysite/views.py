from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import *
from django.db.models import Sum, Value as V, F
from django.db.models.functions import Coalesce


# Create your views here.
def index(request):
    return render(request, "index.html")


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
