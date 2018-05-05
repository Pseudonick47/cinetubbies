from django.db import models


class Category(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=30)
  supercategory = models.ForeignKey(
    to='self',
    on_delete=models.CASCADE,
    related_name='subcategories',
    null=True
  )

  def is_root(self):
    return self.supercategory == None
