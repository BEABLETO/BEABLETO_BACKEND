from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel

from utils.models import DeleteModel, DeleteModelManager


class UserManager(DeleteModelManager, BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if extra_fields.get('type') == User.TYPE_EMAIL:
            username = email
        elif username is None:
            raise ValidationError('사용자 생성 필수값(username)이 주어지지 않았습니다')
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel, DeleteModel):
    TYPE_EMAIL = 'email'
    first_name = None
    last_name = None
    username = None
    email = models.EmailField('이메일', unique=True)
    type = models.CharField('유형', max_length=10, default=TYPE_EMAIL)
    name = models.CharField('이름', max_length=20)
    phone = models.CharField('전화번호', max_length=12, null=True)
    guardian_phone = models.CharField('보호자 전화번호', max_length=12, null=True)
    aids = models.CharField('보조기구', max_length=20)
    push_agree = models.BooleanField('푸시알람동의')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = (
        'name',
        'aids',
        'push_agree',
    )

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        if self.type == self.TYPE_EMAIL:
            self.username = self.email
        super().save(*args, **kwargs)

    def perform_delete(self):
        deleted_count = User.objects.filter(is_deleted=True).count()
        deleted_name = f'deleted_{deleted_count:05d}'
        self.username = deleted_name
        self.nickname = deleted_name

