from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import *


# Create your views here.
def index(request):
    return render(request, "index.html")


def exp(request):
    return render(request, "db-page-exp.html", {
        "img_exp_builder": "/assets/images/1024x640.png",
        "exp_name": "GG20 Align",
        "exp_builder": "warren",
        "exp_intro": "谷歌20实验复现",
        "exp_updates": ["ADD LRP", "ADD CC"],

        "img_updater": "/assets/images/90x90.png",
        "updater": "warren",
        "update_time": "Sept 01, 2018",
        "update_name": "ADD LRP",
        "update_intro": "如图所示，目前已和GG报告的结果对齐",
        "img_update": "/assets/images/1024x640.png",
        "num_comment": "1",

        "comments": Comment.objects,
        # "commenters": ["warren"],
        # "comment_times": ["Sept 01, 2018"],
        # "img_commenters": ["/assets/images/140x140.png"],
        # "comments": ["hdl nb"],

    })
    return render(request, "page-login.html")
