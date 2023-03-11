from django.db import models
from ordered_model import models as ordered_models

from sagittarius.core import models as core_models


class Scoresheet(ordered_models.OrderedModel, core_models.BaseModel):
    group = models.ForeignKey("organize.Group", on_delete=models.CASCADE)
    order_with_respect_to = "group"

    registration = models.ForeignKey(
        "organize.Registration",
        on_delete=models.CASCADE,
    )
    # cache
    score = models.DecimalField(decimal_places=2, max_digits=8)
    arrow_score = models.DecimalField(decimal_places=2, max_digits=8)


class Run(ordered_models.OrderedModel, core_models.BaseModel):
    scoresheet = models.ForeignKey(Scoresheet, on_delete=models.CASCADE)
    order_with_respect_to = "scoresheet"


class ScoreItem(core_models.BaseModel):
    class Types(models.TextChoices):
        TARGET = "target", "Target"
        TIME = "time", "Time"
        BONUS = "bonus", "Bonus/Penalty"
        INCIDENT = "incident", "Incident"

    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=Types.choices)
    value = models.JSONField()
