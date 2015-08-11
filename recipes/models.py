import time
from django.db import models
from cityfarm_api.models import Model
from plants.models import PlantType
from resources.models import ResourceProperty


class Recipe(Model):
    name = models.CharField(max_length=100)
    plant_type = models.ManyToManyField(PlantType, related_name='recipes')
    file = models.FileField(upload_to="recipes")

    def __str__(self):
        return self.name


class RecipeRun(Model):
    class Meta:
        get_latest_by = 'start_timestamp'

    start_timestamp = models.IntegerField(blank=True, default=time.time)
    end_timestamp = models.IntegerField(editable=False)
    recipe = models.ForeignKey(Recipe, related_name='runs')
    tray = models.ForeignKey('layout.Tray', related_name='recipe_runs+')


class SetPoint(Model):
    class Meta:
        get_latest_by = 'timestamp'

    tray = models.ForeignKey('layout.Tray', related_name='set_points+')
    property = models.ForeignKey(ResourceProperty, related_name='set_points+')
    timestamp = models.IntegerField()
    value = models.FloatField(null=True)
    recipe_run = models.ForeignKey(RecipeRun, related_name='set_points+')
