from django.db import models
from django.utils import timezone


# Create your models here.
class MGenre(models.Model):
	title = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	addr = models.CharField(max_length=2000)
	flag = models.IntegerField(default=1)

	def __str__(self):
		return self.title

	class Meta():
		db_table = 'mgenre'


class MInformation(models.Model):
	title = models.CharField(max_length=200)
	sorce = models.CharField(max_length=20)
	name = models.CharField(max_length=100)
	actor = models.CharField(max_length=500)
	ptime = models.CharField(max_length=100)
	language = models.CharField(max_length=200)
	pyear = models.CharField(max_length=20)
	country = models.CharField(max_length=100)
	img = models.CharField(max_length=2000, blank=True)
	create_time = models.DateTimeField(default=timezone.now)
	activator = models.CharField(max_length=100, blank=True)
	summary = models.TextField(blank=True)

	mtype = models.ManyToManyField(MGenre)

	def __str__(self):
		return self.title

	class Meta():
		db_table = 'minformation'


class MIGenre(models.Model):
	title = models.CharField(max_length=200)
	addr = models.CharField(max_length=2000)
	flag = models.IntegerField(default=1)
	mgenre = models.ForeignKey(MGenre, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta():
		db_table = 'migenre'


class MIData(models.Model):
	title = models.CharField(max_length=200)
	addr = models.CharField(max_length=255, db_index=True)
	flag = models.IntegerField(default=1)
	mgenre = models.ForeignKey(MGenre, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta():
		db_table = 'midata'