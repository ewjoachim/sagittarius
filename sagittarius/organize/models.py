import datetime

from django.core import validators
from django.db import models
from django_countries import fields as django_countries_fields
from django_extensions.db import fields as django_ext_fields
from ordered_model import models as ordered_models

from sagittarius.core import models as core_models


class Level(core_models.BaseModel):
    class Stars(models.IntegerChoices):
        ONE_STAR = 1, "One Star"
        TWO_STARS = 2, "Two Stars"
        THREE_STARS = 3, "Three Stars"
        FOUR_STARS = 4, "Four Stars"
        FIVE_STARS = 5, "Five Stars"

    stars = models.SmallIntegerField(choices=Stars.choices, null=True)
    country = django_countries_fields.CountryField(blank=True)
    name = models.CharField(max_length=128, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        if self.name:
            if self.country:
                return f"[{self.country.code}]{self.name}"
            return self.name
        return str(self.stars.label)


class Club(core_models.BaseModel):
    name = models.CharField(max_length=128, blank=True)
    country = django_countries_fields.CountryField(blank=True)


class Horse(core_models.BaseModel):
    name = models.CharField(max_length=128, blank=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(core_models.User, on_delete=models.SET_NULL, null=True)


def thirty_years_ago():
    return datetime.date.today() - datetime.timedelta(years=30)


class Rider(core_models.BaseModel):
    user = models.ForeignKey(core_models.User, on_delete=models.SET_NULL, null=True)
    left_handed = models.BooleanField(default=False)
    birth_year = models.IntegerField(
        default=thirty_years_ago,
        validators=[
            validators.MinValueValidator(1900),
            validators.MaxValueValidator(2050),
        ],
    )
    country = django_countries_fields.CountryField(blank=True)


class RecurringMeeting(core_models.BaseModel):
    name = models.CharField(max_length=128)


class Meeting(core_models.BaseModel):
    name = models.CharField(max_length=128)
    slug = django_ext_fields.AutoSlugField(populate_from="name", overwrite=True)
    is_international = models.BooleanField(default=False)
    location = models.CharField(max_length=128, blank=True)
    country = django_countries_fields.CountryField(blank=True)
    contact = models.ForeignKey(core_models.User, on_delete=models.SET_NULL, null=True)
    website = models.URLField(blank=True)
    date = models.DateField()


class Competition(core_models.BaseModel):
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True)


class Organizer(core_models.BaseModel):
    class Role(models.TextChoices):
        ORGANIZER = "organizer", "Organizer"
        JUDGE = "judge", "Judge"

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    user = models.ForeignKey(core_models.User, on_delete=models.CASCADE)


class Team(core_models.BaseModel):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True)
    country = django_countries_fields.CountryField(blank=True)


class Event(core_models.BaseModel):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    rule_set = models.ForeignKey("rules.RuleSet", on_delete=models.PROTECT)


class Group(ordered_models.OrderedModel, core_models.BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    order_with_respect_to = "event"


class Registration(core_models.BaseModel):
    rider = models.ForeignKey(Rider, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    country = django_countries_fields.CountryField(blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
