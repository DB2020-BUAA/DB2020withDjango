from django.shortcuts import render
import mysite.models as mmd


# Create your views here.
def index(request):
    return render(request, "page-login.html")


def list_diff(request):
    return render(request, "db-page-diff-list-n.html")


def list_group(request, warning=None):
    if request.user.is_authenticated:
        try:
            people_id = request.user.id
            group_list = mmd.UserToGroup.objects. \
                filter(linked_user__django_user_id=people_id). \
                values_list("linked_group__id", "linked_group__name", "linked_group__info")
        except mmd.UserToGroup.DoesNotExist:
            group_list = None
        info_get = {'group_list': group_list, 'warning': warning}
        return render(request, "db-page-group-list.html", info_get)
    else:
        return render(request, "page-login.html")


def group(request, group_id):
    return render(request, "db-page-group.html")


def create_group(request):
    if request.user.is_authenticated:
        master_user = mmd.UserProfile.objects.get(django_user_id=request.user.id)
        try:
            g_name = request.POST['name']
            g_info = request.POST['info']
        except KeyError:
            return list_group(request, warning=False)
        new_group = mmd.Group(name=g_name, info=g_info, owner=master_user)
        try:
            new_group.save()
        except ValueError:
            return list_group(request, warning=False)
        return list_group(request, warning=True)
    else:
        return render(request, "page-login.html")
