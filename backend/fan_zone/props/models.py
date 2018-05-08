from django.db import models


class Prop(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True, default='')
  image = models.ForeignKey(
    to="media_upload.Image",
    on_delete=models.SET_NULL,
    related_name='+',
    null=True
  )
  post_date = models.DateField(auto_now_add=True)

  class Meta:
    abstract = True
