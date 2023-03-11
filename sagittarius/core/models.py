from hashlib import md5

from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        default_permissions = []

    uuid = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(auth_models.AbstractUser):
    # Don't use first_name, last_name, get_full_name

    name = models.CharField(
        max_length=128,
        db_index=True,
        help_text="Full name. Might be the legal name or not. Will be visible "
        "to competition organizers and participants.",
    )

    name = models.CharField(
        max_length=128,
        db_index=True,
        help_text="Public name. Will be displayed to unauthenticated users. "
        "If you'd rather not have your public name displayed, you can use initials.",
    )

    phone_regex = validators.RegexValidator(
        regex=r"^\+\d{9,17}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 17 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    use_gravatar = models.BooleanField(default=True)

    @property
    def gravatar_url(self) -> str | None:
        if not self.use_gravatar:
            return None
        email_hash = md5(self.email.lower()).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"
