from django.db import models
from django.contrib.auth.models import User


def avatar_directory_path(instance: "User", filename: str) -> str:
    return "user/user-{pk}/avatar/{filename}".format(
        pk=instance.user.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=avatar_directory_path,
    )


# def account_avatar_directory_path(instance: "Profile", filename: str) -> str:
#     return "user/user-{pk}/avatar/{filename}".format(
#         pk=instance.user.pk,
#         filename=filename,
#     )
#
#
# class ProfileAvatar(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="avatar")
#     avatar = models.ImageField(null=True, blank=True, upload_to=account_avatar_directory_path)
