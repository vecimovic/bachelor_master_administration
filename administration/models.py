from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
import os

class Role(models.Model):
	"""
    Pohranjuje uloge djelatnika u sustavu.
    """
	#diplomski 
	PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_STROJARSTVO = 1
	ZAMJENIK_POVJERENSTVA_DIPLOMSKI_STROJARSTVO = 2
	DJELOVODA_POVJERENSTVA_DIPLOMSKI_STROJARSTVO = 3

	PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_BRODOGRADNJA = 4  
	ZAMJENIK_POVJERENSTVA_DIPLOMSKI_BRODOGRADNJA = 5
	DJELOVODA_POVJERENSTVA_DIPLOMSKI_BRODOGRADNJA = 6

	PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_ELEKTROTEHNIKA = 7
	ZAMJENIK_POVJERENSTVA_DIPLOMSKI_ELEKTROTEHNIKA = 8
	DJELOVODA_POVJERENSTVA_DIPLOMSKI_ELEKTROTEHNIKA = 9

	PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_RACUNARSTVO = 10
	ZAMJENIK_POVJERENSTVA_DIPLOMSKI_RACUNARSTVO = 11
	DJELOVODA_POVJERENSTVA_DIPLOMSKI_RACUNARSTVO = 12

	#preddiplomski
	PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_STROJARSTVO = 13
	ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_STROJARSTVO = 14
	DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_STROJARSTVO = 15

	PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_BRODOGRADNJA = 16
	ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_BRODOGRADNJA = 17
	DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_BRODOGRADNJA = 18

	PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_ELEKTROTEHNIKA = 19
	ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_ELEKTROTEHNIKA = 20
	DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_ELEKTROTEHNIKA = 21

	PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_RACUNARSTVO = 22
	ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_RACUNARSTVO = 23
	DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_RACUNARSTVO = 24

	#strucni
	PREDSJEDNIK_POVJERENSTVA_STRUCNI_STROJARSTVO = 25
	ZAMJENIK_POVJERENSTVA_STRUCNI_STROJARSTVO = 26
	DJELOVODA_POVJERENSTVA_STRUCNI_STROJARSTVO = 27

	PREDSJEDNIK_POVJERENSTVA_STRUCNI_BRODOGRADNJA = 28
	ZAMJENIK_POVJERENSTVA_STRUCNI_BRODOGRADNJA = 29
	DJELOVODA_POVJERENSTVA_STRUCNI_BRODOGRADNJA = 30

	PREDSJEDNIK_POVJERENSTVA_STRUCNI_ELEKTROTEHNIKA = 31
	ZAMJENIK_POVJERENSTVA_STRUCNI_ELEKTROTEHNIKA = 32
	DJELOVODA_POVJERENSTVA_STRUCNI_ELEKTROTEHNIKA = 33
	MENTOR = 34
	KOMENTOR = 35
	

	ROLE_CHOICES = (

		#diplomski
	    (PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_STROJARSTVO, 'predsjednik povjerenstva za diplomske ispite - strojarstvo'),
	    (ZAMJENIK_POVJERENSTVA_DIPLOMSKI_STROJARSTVO, 'zamjenik povjerenstva za diplomske ispite - strojarstvo'),
	    (DJELOVODA_POVJERENSTVA_DIPLOMSKI_STROJARSTVO, 'djelovođa povjerenstva za diplomske ispite - strojarstvo'),

	    (PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_BRODOGRADNJA, 'predsjednik povjerenstva za diplomske ispite - brodogradnja'),
	    (ZAMJENIK_POVJERENSTVA_DIPLOMSKI_BRODOGRADNJA, 'zamjenik povjerenstva za diplomske ispite - brodogradnja'),
	    (DJELOVODA_POVJERENSTVA_DIPLOMSKI_BRODOGRADNJA, 'djelovođa povjerenstva za diplomske ispite - brodogradnja'),

	    (PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_ELEKTROTEHNIKA, 'predsjednik povjerenstva za diplomske ispite - elektrotehnika'),
	    (ZAMJENIK_POVJERENSTVA_DIPLOMSKI_ELEKTROTEHNIKA, 'zamjenik povjerenstva za diplomske ispite - elektrotehnika'),
	    (DJELOVODA_POVJERENSTVA_DIPLOMSKI_ELEKTROTEHNIKA, 'djelovođa povjerenstva za diplomske ispite - elektrotehnika'),

	    (PREDSJEDNIK_POVJERENSTVA_DIPLOMSKI_RACUNARSTVO, 'predsjednik povjerenstva za diplomske ispite - računarstvo'),
	    (ZAMJENIK_POVJERENSTVA_DIPLOMSKI_RACUNARSTVO, 'zamjenik povjerenstva za diplomske ispite - računarstvo'),
	    (DJELOVODA_POVJERENSTVA_DIPLOMSKI_RACUNARSTVO, 'djelovođa povjerenstva za diplomske ispite - računarstvo'),

	    #preddiplomski
	    (PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_STROJARSTVO, 'predsjednik povjerenstva za završne ispite - strojarstvo sveučilišni'),
	    (ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_STROJARSTVO, 'zamjenik povjerenstva za završne ispite - strojarstvo sveučilišni'),
	    (DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_STROJARSTVO, 'djelovođa povjerenstva za završne ispite - strojarstvo sveučilišni'),

	    (PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_BRODOGRADNJA, 'predsjednik povjerenstva za završne ispite - brodogradnja sveučilišni'),
	    (ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_BRODOGRADNJA, 'zamjenik povjerenstva za završne ispite - brodogradnja sveučilišni'),
	    (DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_BRODOGRADNJA, 'djelovođa povjerenstva za završne ispite - brodogradnja sveučilišni'),

	    (PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_ELEKTROTEHNIKA, 'predsjednik povjerenstva za završne ispite - elektrotehnika sveučilišni'),
	    (ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_ELEKTROTEHNIKA, 'zamjenik povjerenstva za završne ispite - elektrotehnika sveučilišni'),
	    (DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_ELEKTROTEHNIKA, 'djelovođa povjerenstva za završne ispite - elektrotehnika sveučilišni'),

	    (PREDSJEDNIK_POVJERENSTVA_PREDDIPLOMSKI_RACUNARSTVO, 'predsjednik povjerenstva za završne ispite - računarstvo sveučilišni'),
	    (ZAMJENIK_POVJERENSTVA_PREDDIPLOMSKI_RACUNARSTVO, 'zamjenik povjerenstva za završne ispite - računarstvo sveučilišni'),
	    (DJELOVODA_POVJERENSTVA_PREDDIPLOMSKI_RACUNARSTVO, 'djelovođa povjerenstva za završne ispite - računarstvo sveučilišni'),

	    #strucni
	    (PREDSJEDNIK_POVJERENSTVA_STRUCNI_STROJARSTVO, 'predsjednik povjerenstva za završne ispite - strojarstvo stručni'),
	    (ZAMJENIK_POVJERENSTVA_STRUCNI_STROJARSTVO, 'zamjenik povjerenstva za završne ispite - strojarstvo stručni'),
	    (DJELOVODA_POVJERENSTVA_STRUCNI_STROJARSTVO, 'djelovođa povjerenstva za završne ispite - strojarstvo stručni'),

	    (PREDSJEDNIK_POVJERENSTVA_STRUCNI_BRODOGRADNJA, 'predsjednik povjerenstva za završne ispite - brodogradnja stručni'),
	    (ZAMJENIK_POVJERENSTVA_STRUCNI_BRODOGRADNJA, 'zamjenik povjerenstva za završne ispite - brodogradnja stručni'),
	    (DJELOVODA_POVJERENSTVA_STRUCNI_BRODOGRADNJA, 'djelovođa povjerenstva za završne ispite - brodogradnja stručni'),

	    (PREDSJEDNIK_POVJERENSTVA_STRUCNI_ELEKTROTEHNIKA, 'predsjednik povjerenstva za završne ispite - elektrotehnika stručni'),
	    (ZAMJENIK_POVJERENSTVA_STRUCNI_ELEKTROTEHNIKA, 'zamjenik povjerenstva za završne ispite - elektrotehnika stručni'),
	    (DJELOVODA_POVJERENSTVA_STRUCNI_ELEKTROTEHNIKA, 'djelovođa povjerenstva za završne ispite - elektrotehnika stručni'),
	    (MENTOR, 'mentor'),
	    (KOMENTOR, 'komentor'),

	)

	id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

	def __str__(self):
		"""
		Prikazuje ulogu u bazi u obliku stringa kao ime uloge.
		"""
		return self.get_id_display()

class Student(models.Model):
	"""
    Pohranjuje studente u sustavu,
    u relaciji sa :model:`auth.User`.
    """ 
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	area_of_study = models.CharField(max_length=50)
	category = models.CharField(max_length=50)
	jmbag = models.CharField(max_length=50)
	def __str__ (self):
		"""
		Prikazuje studenta u bazi u obliku stringa kao ime i prezime studenta.
		"""
		return self.user.first_name + " " + self.user.last_name

class Employee(models.Model):
	"""
    Pohranjuje djelatnike u sustavu,
    u relaciji sa: :model:`auth.User`, :model:`administration.Role`.
    """ 
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	roles = models.ManyToManyField(Role)

	def __str__ (self):
		"""
		Prikazuje djelatnika u bazi u obliku stringa kao ime i prezime djelatnika.
		"""
		return self.user.first_name + " " + self.user.last_name

class Study(models.Model):
	"""
    Pohranjuje nazive svih studija fakulteta u sustav.
    """ 
	#diplomski
	DIPLOMSKI_SVEUCILISNI_STROJARSTVO = 1
	DIPLOMSKI_SVEUCILISNI_BRODOGRADNJA = 2
	DIPLOMSKI_SVEUCILISNI_ELEKTROTEHNIKA = 3
	DIPLOMSKI_SVEUCILISNI_RACUNARSTVO = 4

	#preddiplomski
	PREDDIPLOMSKI_SVEUCILISNI_STROJARSTVO = 5
	PREDDIPLOMSKI_SVEUCILISNI_BRODOGRADNJA = 6
	PREDDIPLOMSKI_SVEUCILISNI_ELEKTROTEHNIKA = 7
	PREDDIPLOMSKI_SVEUCILISNI_RACUNARSTVO = 8
	
	#strucni
	STRUCNI_STROJARSTVO = 9
	STRUCNI_BRODOGRADNJA = 10
	STRUCNI_ELEKTROTEHNIKA = 11

	STUDY_CHOICES = (
		#diplomski
		(DIPLOMSKI_SVEUCILISNI_STROJARSTVO, 'Diplomski sveučilišni studij strojarstvo'),
		(DIPLOMSKI_SVEUCILISNI_BRODOGRADNJA, 'Diplomski sveučilišni studij brodogradnja'),
		(DIPLOMSKI_SVEUCILISNI_ELEKTROTEHNIKA, 'Diplomski sveučilišni studij elektrotehnika'),
		(DIPLOMSKI_SVEUCILISNI_RACUNARSTVO, 'Diplomski sveučilišni studij računarstvo'),

		#preddiplomski
		(PREDDIPLOMSKI_SVEUCILISNI_STROJARSTVO, 'Preddiplomski sveučilišni studij strojarstvo'),
		(PREDDIPLOMSKI_SVEUCILISNI_BRODOGRADNJA, 'Preddiplomski sveučilišni studij brodogradnja'),
		(PREDDIPLOMSKI_SVEUCILISNI_ELEKTROTEHNIKA, 'Preddiplomski sveučilišni studij elektrotehnika'),
		(PREDDIPLOMSKI_SVEUCILISNI_RACUNARSTVO, 'Preddiplomski sveučilišni studij računarstvo'),
		#strucni
		(STRUCNI_STROJARSTVO, 'Preddiplomski stručni studij strojarstvo'),
		(STRUCNI_BRODOGRADNJA, 'Preddiplomski stručni studij brodogradnja'),
		(STRUCNI_ELEKTROTEHNIKA, 'Preddiplomski stručni studij elektrotehnika'),
	)

	id = models.PositiveSmallIntegerField(choices=STUDY_CHOICES, primary_key=True)

	def __str__(self):
		"""
		Prikazuje studij u bazi u obliku stringa kao ime studija.
		"""
		return self.get_id_display()

	class Meta:
		verbose_name_plural = "studies"

class Thesis(models.Model):
	"""
    Pohranjuje završne i diplomske radove u sustavu,
    u relaciji sa: :model:`administration.Student`, :model:`administration.Employee`, :model:`administration.Study`.
    """ 
	#tip
	ZAVRSNI = 1
	DIPLOMSKI = 2

	TYPE_CHOICES = (
		(ZAVRSNI, 'Završni rad'),
		(DIPLOMSKI, 'Diplomski rad'),
	)

	#status
	SPREMLJEN = 1
	PREDAN_MENTORU = 2
	PROVJEREN = 3
	PREDAN_POVJERENSTVU = 4
	PRIHVACEN = 5
	ODBIJEN = 6
	U_DORADI = 7
	OBRANJEN = 8
	NIJE_POLOŽEN = 9

	STATUS_CHOICES = (
		(SPREMLJEN, 'SPREMLJEN'),
		(PREDAN_MENTORU, 'PREDAN MENTORU'),
		(PROVJEREN, 'PROVJEREN'),
		(PREDAN_POVJERENSTVU, 'PREDAN POVJERENSTVU'),
		(PRIHVACEN, 'PRIHVAĆEN'),
		(ODBIJEN, 'ODBIJEN'),
		(U_DORADI, 'U DORADI'),
		(OBRANJEN, 'OBRANJEN'),
		(NIJE_POLOŽEN, 'NIJE POLOŽEN')

	)

	title = models.CharField(max_length=100)
	title_english = models.CharField(max_length=100,default=" ")
	summary = models.TextField(default=" ")
	summary_english = models.TextField(default=" ")
	author = models.ForeignKey(Student, on_delete=models.CASCADE)
	mentor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='mentor')
	komentor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='komentor', blank=True, null=True)
	president_of_thesis_comitee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='predsjednik_povjerenstva', null=True)
	deputy_of_thesis_comitee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='zamjenik_povjerenstva', null=True)
	writer_of_thesis_comitee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='djelovođa_povjerenstva', null=True)
	study = models.ForeignKey(Study, on_delete=models.CASCADE)
	file = models.FileField(blank=True)
	type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
	remark = models.TextField(blank=True)
	date = models.DateField(default=timezone.now())
	verification_of_authenticity = models.FileField(blank=True)
	final_grade = models.IntegerField(blank=True,null=True)

	class Meta:
		verbose_name_plural = "theses"
	
	def __str__ (self):
		"""
		Prikazuje rad u bazi u obliku stringa kao naslov rada.
		"""
		return self.title

class MemberOfThesisComitee(models.Model):
	"""
    Pohranjuje članove povjerenstva i njihove ocjene za određeni diplomski rad u sustavu,
    u relaciji sa: :model:`administration.Thesis`, :model:`administration.Employee`.
    """ 
	thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE)
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	grade = models.IntegerField(blank=True, null=True)
	defense_grade = models.IntegerField(blank=True,null=True)

	def __str__ (self):
		"""
		Prikazuje članove povjerenstva u bazi u obliku stringa kao ime i prezime člana.
		"""
		return self.employee.user.first_name + " " + self.employee.user.last_name

class Notification(models.Model):
	"""
    Pohranjuje obavijesti korisnika u sustavu,
    u relaciji sa: :model:`auth.User`.
    """
	SENT = 1
	READ = 2

	STATUS_CHOICES = {
		(SENT, 'SENT'),
		(READ, 'READ'),
	}
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=1000)
	content = models.TextField()
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
	date = models.DateTimeField(default=timezone.now())

	def __str__ (self):
		"""
		Prikazuje obavijesti u bazi u obliku stringa kao naslov obavijesti.
		"""
		return self.title