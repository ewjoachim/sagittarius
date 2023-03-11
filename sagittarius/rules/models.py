from django.db import models

from sagittarius.core import models as core_models


class Discipline(core_models.BaseModel):
    name = models.CharField(max_length=128)


class RuleSet(core_models.BaseModel):
    discipline = models.ForeignKey(Discipline, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=128)
    ihaa_official = models.BooleanField(default=False)
    interface_code = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    rules = models.JSONField()
