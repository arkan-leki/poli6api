from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.aggregates import Max
from ckeditor.fields import RichTextField

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30)
    phoneid = models.CharField(max_length=110, default='Unknown')
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'phoneid']

    objects = MyAccountManager()

    def __str__(self):
        return str(self.username)

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    @property
    def highscore(self):
        quizes = Quize.objects.all()

        if self.r_user.all:
            quizetotallSells = {}
            for quize in quizes:
                score = 0
                if (self.r_user.exists):
                    score = self.r_user.filter(quize=quize.id).aggregate(
                        (Max('score')))['score__max'] or 0

                quizetotallSells[quize.id] = score
        return quizetotallSells

    @property
    def scores(self):
        score = 0
        for scores in self.highscore:
            score = score + self.highscore[scores]
        return score

    class Meta:
        verbose_name_plural = "هه‌ژمار"


class Quize(models.Model):
    category = models.CharField("ناو", max_length=110)
    imageURL = models.CharField("وێنە", max_length=300, null=True, blank=True)
    questions = models.CharField(
        "ژمارەی پرسیارەکان", max_length=11, null=True, blank=True)

    def __str__(self):
        return str(self.category)

    def get_questioons(self):
        return self.q_quize.all()

    @property
    def top_scores(self):
        return self.r_quize.all().filter(score__gte=0).order_by('-score')[:10]

    class Meta:
        verbose_name_plural = "وانەکان"


class Question(models.Model):
    text = RichTextField("پرسیار")
    quize = models.ForeignKey(
        Quize, related_name="q_quize", on_delete=models.CASCADE, verbose_name="وانە")
    date_create = models.DateField(
        verbose_name="بەروار", auto_now_add=True, blank=True)
    add_date = models.DateTimeField(
        verbose_name='رێکەوت', auto_now=True, blank=True)

    def __str__(self):
        return f"user{self.pk}  {self.quize}"

    @property
    def correct_answare(self):
        return self.a_question.get(correct=True)

    def get_answare(self):
        return self.a_question.all()

    class Meta:
        verbose_name_plural = "پرسیارەکان"


class Answare(models.Model):
    text = models.CharField("هەڵبژاردن", max_length=200)
    correct = models.BooleanField("وەڵامی دروست", default=False)
    question = models.ForeignKey(
        Question, related_name="a_question", on_delete=models.CASCADE, verbose_name="prsyar")

    def __str__(self):
        return str(self.text)

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "وەڵامەکان"


class Result(models.Model):
    quize = models.ForeignKey(
        Quize, related_name="r_quize", on_delete=models.CASCADE)
    user = models.ForeignKey(
        Account, related_name="r_user", on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"user{self.user} @ {self.quize} = {self.score}"

    def __unicode__(self):
        return

    class Meta:
        verbose_name_plural = "ئەنجامەکان"
