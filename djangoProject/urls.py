"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite.views import *

from mysite import views

urlpatterns = [
    path('init_all', init_all),
    path('admin/', admin.site.urls),
    # path('', index),
    path('exp/', exp),

    path('exp/cmt_upd/<str:upd_id>', cmt_upd),
    path('exp/cmt_cmp/<str:cmp_id>', cmt_cmp),
    path('exp/my_upd/<int:exp_id>', my_upd),
    path('exp/my_iss', my_iss),

    path('', views.index, name="main"),

    path('login', views.login_page, name='login'),
    path('login/<str:info>/<int:i_type>', views.login_page, name='login_redirect'),
    path('login-sign-in', views.sign_in, name='sign_in'),
    path('login-sign-out', views.sign_out, name='sign_out'),
    path('login-sign-up', views.sign_up, name='sign_up'),
    path('login-register', views.register_page, name='register'),
    path('login-register/<str:info>/<int:i_type>', views.register_page, name='register_redirect'),

    path('group/<int:group_id>', views.group, name="group"),  # TODO: link to group page

    path('group-list', views.list_group, name="group_list"),
    path('group-list-create', views.create_group, name='group_create'),
    path('group-list/<str:warning>/<int:w_type>', views.list_group, name="group_list_redirect"),

    path('diff-list', views.list_diff, name="diff_list"),
    path('diff-list/<str:warning>/<int:w_type>', views.list_diff, name="diff_list_redirect"),
    path('diff-list-delete/<int:diff_id>', views.delete_diff, name='diff_delete'),

    path('exps-list', views.list_exps, name="exps_list"),
    path('exps-list/<str:warning>/<int:w_type>', views.list_exps, name="exps_list_redirect"),
    path('exps-list-delete/<int:exp_id>', views.delete_exps, name='exps_delete'),
]

handler404 = 'mysite.views.page_not_found'
