from django.db import models
from django.contrib.auth.models import User


def user_avatar_path(instance, filename):
    # avatar will be uploaded to MEDIA_ROOT/avatar/user_<id>_<filename>
    return 'avatar/user_{0}_{1}'.format(instance.name, filename)


def user_data_path(instance, filename):
    # avatar will be uploaded to MEDIA_ROOT/data/user_<id>/<filename>
    return 'data/{0}/{1}'.format(instance.create_user, filename)


class UserProfile(models.Model):

    django_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    info = models.TextField(max_length=100, null=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'user_' + self.id.__str__() + '_' + self.django_user.__str__()


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    info = models.TextField(max_length=100, null=True)
    create_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT,
                              related_name='group_master')

    def __str__(self):
        return self.id.__str__() + ':\t' + self.name.__str__()


class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL,
                                    related_name='exp_creator')
    info = models.TextField()
    name = models.TextField(default="default")

    def __str__(self):
        return 'Experiment' + self.id.__str__() + ': ' + self.name.__str__()


class Update(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL,
                                    related_name='update_creator')
    info = models.TextField()
    name = models.TextField(default="default")
    imgs = models.TextField(default="")

    def __str__(self):
        return 'Update' + self.id.__str__() + ': ' + self.create_date.__str__()


class UpdateData(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL,
                                    related_name='data_creator')
    info = models.TextField()
    name = models.TextField(default="default")
    data = models.FileField(upload_to=user_data_path)
    file_type = models.CharField(max_length=6, null=True)

    def __str__(self):
        return 'data_' + self.id.__str__() + '_' + self.create_date.__str__()


class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE,
                                    related_name='issue_creator')
    target_update = models.ForeignKey(Update, on_delete=models.CASCADE)
    info = models.TextField()
    status = models.IntegerField(default=0)
    answer_date = models.DateTimeField(auto_now=True)
    answer_info = models.TextField(null=True, default='have not been answered')

    def __str__(self):
        return 'issue_' + self.id.__str__() + ' from ' + self.create_user.__str__()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL,
                                    related_name='comment_creator')
    target_update = models.ForeignKey(Update, on_delete=models.CASCADE)
    info = models.TextField()

    def __str__(self):
        return 'comment_' + self.id.__str__() + '_' + self.create_date.__str__()


class Apply(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE,
                                    related_name='apply_creator')
    target_group = models.ForeignKey(Group, on_delete=models.CASCADE,
                                     related_name='apply_target')
    info = models.TextField()
    status = models.IntegerField(default=0)
    reply_time = models.DateTimeField(auto_now=True)
    reply = models.BooleanField(default=False)

    def __str__(self):
        return 'apply' + self.create_user.__str__() + 'to' + self.target_group.__str__()


class Compare(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL,
                                    related_name='compare_creator')
    upd1 = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='compare_update1')
    upd2 = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='compare_update2')
    info = models.TextField()
    name = models.TextField()
    imgs = models.TextField(default="")

    def __str__(self):
        return 'compare' + self.upd1.__str__() + ' and ' + self.upd2.__str__()


class CMPComment(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(UserProfile, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='cmp_comment_creator')
    target_cmp = models.ForeignKey(Compare,
                                   on_delete=models.CASCADE)
    info = models.TextField()

    def __str__(self):
        return 'comment_' + self.id.__str__() + '_' + self.create_date.__str__()


class UserToGroup(models.Model):
    id = models.AutoField(primary_key=True)
    linked_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    linked_group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.linked_user.__str__() + ' in ' + self.linked_group.__str__()


class ExpToGroup(models.Model):
    id = models.AutoField(primary_key=True)
    linked_exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    linked_group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.linked_exp.__str__() + ' in ' + self.linked_group.__str__()


class UpdToExp(models.Model):
    id = models.AutoField(primary_key=True)
    linked_exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    linked_upd = models.ForeignKey(Update, on_delete=models.CASCADE)

    def __str__(self):
        return self.linked_upd.__str__() + ' in ' + self.linked_exp.__str__()


class DataToUpd(models.Model):
    id = models.AutoField(primary_key=True)
    linked_data = models.ForeignKey(UpdateData, on_delete=models.CASCADE)
    linked_upd = models.ForeignKey(Update, on_delete=models.CASCADE)

    def __str__(self):
        return self.linked_upd.__str__() + ' in ' + self.linked_data.__str__()
