from django.db import models


class Category(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=30)
  supercategory = models.ForeignKey(
    to='self',
    on_delete=models.CASCADE,
    related_name='subcategories',
    null=True
  )

  def is_root(self):
    return self.supercategory == None


class Prop(models.Model):
  id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True, default='')
  category = models.ForeignKey(
    to=Category,
    on_delete=models.PROTECT,
    related_name='officialprops'
  )
  image = models.ForeignKey(
    to="media_upload.Image",
    on_delete=models.SET_NULL,
    related_name='+',
    null=True
  )


class OfficialProp(Prop):
  theater = models.ForeignKey(
    to='theaters.Theater',
    on_delete=models.CASCADE,
    related_name='officialprops'
  ),
  quantity = models.IntegerField(
    blank=False,
    null=False
  )
  price = models.FloatField(
    blank=False,
    null=False
  )