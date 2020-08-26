import os
from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    nickName = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

def date_upload_to(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    # ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    # uuid_name = uuid4().hex
    # 확장자 추출
    uuid_name = 'photo/'
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([
        # ymd_path,
        uuid_name + instance.userEmail + extension,
    ])

class Users(models.Model):
    userEmail = models.EmailField(max_length=30, primary_key=True, verbose_name="이메일(아이디)")
    nickName = models.CharField(max_length=12, verbose_name="닉네임")
    password = models.CharField(max_length=12, verbose_name="비밀번호")
    registerDate = models.DateField(auto_now_add=True, verbose_name="가입시간")
#    photo = models.ImageField(blank=True, height_field=50, width_field=50, upload_to=date_upload_to)
    photo = models.FileField(blank=True, upload_to=date_upload_to)
    guardianName = models.CharField(blank=True, max_length=12, verbose_name="보호자명")
    guardianCallNum = models.CharField(blank=True, max_length=12, verbose_name="보호자전화번호")
    guardianBasicMsg = models.CharField(blank=True, max_length=100, verbose_name="보호자기본메세지")
    def __str__(self):
        return  f"[{self.__class__.__name__}] userEmail={self.userEmail}"

