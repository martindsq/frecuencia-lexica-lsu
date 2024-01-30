from django.apps import AppConfig
from .options import FrequenciesOptions
from django.utils.translation import gettext_lazy as _

class FrequenciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frequencies'
    options = FrequenciesOptions()
    verbose_name = _('Frequencies')
