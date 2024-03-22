from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _

class Stimulus(models.Model):
	term = models.CharField(max_length=50, verbose_name=_('Term'))
	file_name = models.CharField(max_length=50, verbose_name=_('Filename'))
	is_active = models.BooleanField(default=True, verbose_name=_('Is active'))

	class Meta:
		verbose_name = _('Stimulus')
		verbose_name_plural = _('Stimuli')
	
	def __str__(self):
		return self.file_name

class Form(models.Model):
	class Birthplace(models.TextChoices):
		SOUTH = 'South', 'Sur (Montevideo o Canelones)'
		WEST = 'West', 'Oeste (San José, Soriano, Colonia o Río Negro)'
		CENTER = 'Center', 'Centro (Durazno, Flores, Florida o Lavalleja)'
		NORTH = 'North', 'Norte (Artigas, Salto, Paysandú, Tacuarembó o Rivera)'
		EAST = 'East', 'Este (Rocha, Maldonado, Cerro Largo o Treinta y Tres)'
		ARGENTINA = 'Argentina', 'Argentina'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class AgeofAcquisition(models.TextChoices):
		AT_BIRTH = "Birth", 'De nacimiento'
		BY_6_YEARS_OLD = "<6", 'Antes de los 6 años'
		BY_12_YEARS_OLD = "<12", 'Antes de los 12 años'
		BY_18_YEARS_OLD = "<18", 'Antes de los 18 años'
		AFTER_18_YEARS_OLD = "18>", 'Después de los 18 años'
		NA = "N/A", 'Prefiero no responder'

	class Sex(models.TextChoices):
		MALE = "Male", 'Hombre'
		FEMALE = "Female", 'Mujer'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class Ethnicity(models.TextChoices):
		WHITE = "White", 'Blanca'
		BLACK = "Black", 'Afro o negra'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class DeafCommunity(models.TextChoices):
		YES = "Yes", 'Si'
		NO = "No", 'No'
		NA = "N/A", 'Prefiero no responder'

	class PreferredLanguage(models.TextChoices):
		LSU = "LSU", 'LSU'
		SPANISH = "Spanish", 'Español'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class Language(models.TextChoices):
		LSU = "LSU", 'LSU'
		SPANISH = "Spanish", 'Español'
		GESTURES = "Gestures", 'Mímica'
		FINGERSPELLING = "Fingerspelling", 'Deletreo'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class Education(models.TextChoices):
		SCHOOL = "School", 'Escuela'
		FIRST_CYCLE = "First Cycle", 'Educación media básica (3º de liceo terminado o similar)'
		SECONDARY = "Secondary education", 'Educación media superior (6º de liceo terminado o similar)'
		TERTIARY = "Tertiary education", 'Educación terciaria (tecnicatura, diplomatura o grado universitario)'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class School(models.TextChoices):
		COMMON_SCHOOL = "Common school", 'Escuela común'
		DEAF_CLASS = "Deaf class", 'Clase para sordos en una escuela común'
		BILINGUAL_SCHOOL = "Bilingual school", 'Escuela bilingüe (Nº 197 de Montevideo, Nª 84 de Maldonado, Nº 105 de Rivera, Nª 116 de Salto)'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class Mode(models.IntegerChoices):
		ONLINE = 1, 'En línea'
		OFFLINE = 2, 'Fuera de línea'
		DEBUG = 3, 'Desarrollo'

	guid = models.CharField(primary_key=True, max_length=32)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
	test_mode = models.IntegerField(choices=Mode.choices, verbose_name=_('Mode'))
	is_mobile = models.BooleanField(default=False, verbose_name=_('Is mobile'))
	browser = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Browser'))
	operating_system = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Operating system'))
	name = models.CharField(max_length=50, verbose_name=_('Name'))
	contact = models.CharField(blank=True, max_length=100, verbose_name=_('Contact'))
	sex = models.CharField(max_length=10, choices=Sex.choices, verbose_name=_('Sex'))
	ethnicity = models.CharField(max_length=10, choices=Ethnicity.choices, verbose_name=_('Ethnicity'))
	deaf_community = models.CharField(max_length=5, choices=DeafCommunity.choices, verbose_name=_('Deaf community'))
	birthdate = models.CharField(max_length=4, verbose_name=_('Birthdate'))
	birthplace = models.CharField(max_length=10, choices=Birthplace.choices, verbose_name=_('Birthplace'))
	education = models.CharField(max_length=30, choices=Education.choices, verbose_name=_('Education'))
	school = models.CharField(max_length=20, choices=School.choices, verbose_name=_('School'))
	age_of_acquisition = models.CharField(max_length=5, choices=AgeofAcquisition.choices, verbose_name=_('Age of Acquisition'))
	age_of_acquisition = models.CharField(max_length=5, choices=AgeofAcquisition.choices, verbose_name=_('Age of Acquisition'))
	language_at_home = models.CharField(max_length=20, choices=Language.choices, verbose_name=_('Language at home'))
	lsu_fluency = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name=_('LSU fluency'))
	preferred_language = models.CharField(max_length=20, choices=PreferredLanguage.choices, verbose_name=_('Preferred language'), default=PreferredLanguage.NA)

	class Meta:
		verbose_name = _('Form')
		verbose_name_plural = _('Forms')

	def __str__(self):
		return self.guid

class Reply(models.Model):
	form = models.ForeignKey(Form, related_name='replies', on_delete=models.CASCADE, verbose_name=_('Form'))
	stimulus = models.ForeignKey(Stimulus, on_delete=models.CASCADE, verbose_name=_('Stimulus'))
	familiarity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name=_('Familiarity'))
	rt = models.IntegerField(null=True, blank=True, verbose_name=_('Response time'))
	te = models.IntegerField(null=True, blank=True, verbose_name=_('Time elapsed'))

	class Meta:
		verbose_name = _('Reply')
		verbose_name_plural = _('Replies')
		unique_together = ('form', 'stimulus')
