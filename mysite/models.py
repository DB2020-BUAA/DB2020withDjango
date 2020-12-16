from django.db import models


def user_avatar_path(instance, filename):
    # avatar will be uploaded to MEDIA_ROOT/avatar/user_<id>_<filename>
    return 'avatar/user_{0}_{1}'.format(instance.name, filename)


def user_data_path(instance, filename):
    # avatar will be uploaded to MEDIA_ROOT/data/user_<id>/<filename>
    return 'data/{0}/{1}'.format(instance.create_user, filename)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    info = models.TextField(max_length=100, null=True)
    avatar = models.ImageField(null=True, upload_to=user_avatar_path)

    def __str__(self):
        return 'user_' + self.id.__str__() + '_' + self.name.__str__()


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    info = models.TextField(max_length=100, null=True)
    create_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.id.__str__() + ':\t' + self.name.__str__()


class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateField(auto_now_add=True)
    create_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    info = models.TextField()

    def __str__(self):
        return self.id.__str__() + self.create_date.__str__()


class Update(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    info = models.TextField()

    def __str__(self):
        return self.id.__str__() + self.create_date.__str__()


class UpdateData(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    info = models.TextField()
    data = models.FileField(upload_to=user_data_path)
    file_type = models.CharField(max_length=6, null=True)

    def __str__(self):
        return 'data_' + self.id.__str__() + '_' + self.create_date.__str__()


class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=False)
    answer_date = models.DateTimeField(auto_now=True)
    answer_info = models.TextField()

    def __str__(self):
        return 'issue_' + self.id.__str__() + self.create_date.__str__()

