from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.fields import IntegerField


# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_image', null=True, blank=True)
    mobile = models.CharField(max_length=10, null=False)

    GENDER = (('Male', 'MALE'), ('Female', 'FEMALE'),
              ('Other', 'OTHER'), ('Prefer not to say', 'PREFER NOT TO SAY'))
    gender = models.CharField(max_length=50, choices=GENDER, default=None)
    date_of_birth = models.CharField(max_length=50)
    country = models.CharField(max_length=20, null=False)
    city = models.CharField(max_length=20, null=False)
    college = models.CharField(max_length=100, null=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


class Contact(models.Model):
    Firstname = models.CharField(max_length=34, null=True)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=14)
    message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.Firstname + ' -' + self.email


class QuestionMake(models.Model):

    # for uploading in dynamic path
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'Questions/{0}/{1}'.format(instance.problem_name, filename)

    created_on = models.DateTimeField(auto_now_add=True)
    problem_name = models.CharField(max_length=1000, blank=True, unique=True)
    authorname = models.CharField(max_length=1000, blank=True)
    problem_statement = models.TextField(blank=True, null=True)
    input_format = models.TextField(max_length=1000, blank=True)
    constraints = models.TextField(max_length=1000, blank=True)
    output_format = models.TextField(max_length=1000, blank=True)
    tags = models.TextField(max_length=1000, blank=True)
    sample_input = models.TextField(max_length=1000, blank=True)
    sample_output = models.TextField(max_length=1000, blank=True)
    explanation = models.TextField(max_length=1000, blank=True)
    hidden_input = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    hidden_output = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    difficulty = models.CharField(max_length=20, blank=True)

    def _str_(self):
        return self.problem_name


class ContestInformation(models.Model):
    cname = models.CharField(max_length=100, blank=False, unique=True)
    username = models.CharField(max_length=100, blank=False)
    passcode = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    date = models.DateField(max_length=100)
    starttime = models.TimeField(max_length=100)
    endtime = models.TimeField(max_length=100)
    rules = models.TextField(max_length=1000, blank=False)
    prizes = models.TextField(max_length=1000, blank=False)

    def __str__(self):
        return self.cname


class ContestQuestions(models.Model):
    contest_name = models.ForeignKey(ContestInformation, on_delete=models.SET_NULL, blank=True, null=True)
    questions = models.ManyToManyField('QuestionMake', related_name='question', blank=True)

    def __str__(self):
        return str(self.contest_name)


class ContestUsers(models.Model):
    contest_na = models.ForeignKey(
        ContestQuestions, on_delete=models.SET_NULL, blank=True, null=True)
    username = models.ManyToManyField(
        'UserInfo', related_name='username', blank=False)


class Submissions(models.Model):
    name_of_contest = models.ForeignKey(
        ContestQuestions, on_delete=models.SET_NULL, blank=True, null=True)
    name_of_question = models.CharField(max_length=1000, blank=True)
    name_of_user = models.CharField(max_length=1000, blank=True)
    code = models.TextField(max_length=100000, blank=True)
    language = models.CharField(max_length=1000, blank=True)
    dt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    remaining_time_in_sec = models.IntegerField(default=0)


class LeaderBoard(models.Model):
    con_name = models.ForeignKey(
        ContestQuestions, on_delete=models.SET_NULL, blank=True, null=True)
    uname = models.CharField(max_length=70)
    final_points = models.IntegerField(default=0)
    cumulative_score = models.IntegerField(default=0)
    number_of_submissions = models.IntegerField(default=0)
    successful_submissions = models.IntegerField(default=0)
    college_name = models.CharField(max_length=80, default="Nan")
