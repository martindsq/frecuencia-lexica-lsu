from django.http import HttpResponse
from django.template import loader
from django.templatetags.static import static
from django.utils.translation import gettext as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .models import Form, Stimulus
from .apps import FrequenciesConfig
from .serializers import FormAndRepliesSerializer, StimulusSerializer
from .permissions import IsAdminOrWriteOnly
from django.views.decorators.csrf import csrf_protect

class FormViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormAndRepliesSerializer
    permission_classes = [IsAdminOrWriteOnly]

class StimulusViewSet(ModelViewSet):
    queryset = Stimulus.objects.all()
    serializer_class = StimulusSerializer

@csrf_protect
def index(request):
	try:
		mode = Form.Mode(int(request.GET.get('mode', 1)))
	except ValueError:
		mode = Form.Mode.ONLINE
	
	options = FrequenciesConfig.options
	
	template = loader.get_template('index.html')
	context = {
    	'survey_steps': [
    		{
    			'label': '¿Cómo te llamas?',
    			'hint': 'name',
    			'type': 'text',
    			'required': True
    		},
    		{
    			'label': '¿Cual es tu e-mail o número te teléfono? (opcional)',
    			'hint': 'contact',
    			'type': 'text',
    			'required': False
    		},
    		{
    			'label': '¿Con qué género te identificas mejor?',
    			'hint': 'sex',
    			'type': 'radio',
    			'required': True,
    			'options': Form.Sex.choices
    		},
    		{
    			'label': '¿En qué año naciste?',
    			'hint': 'birthdate',
    			'type': 'select',
    			'required': True,
    			'options': reversed(range(1900, 2023))
    		},
    		{
    			'label': '¿Dónde naciste?',
    			'hint': 'birthplace',
    			'type': 'radio',
    			'required': True,
    			'options': Form.Birthplace.choices
    		},
    		{
    			'label': '¿Te identificas como parte de la comunidad sorda?',
    			'hint': 'deaf_community',
    			'type': 'radio',
    			'required': True,
    			'options': Form.DeafCommunity.choices
    		},
    		{
    			'label': '¿Con qué etnia te identificas mejor?',
    			'hint': 'ethnicity',
    			'type': 'radio',
    			'required': True,
    			'options': Form.Ethnicity.choices
    		},
    		{
    			'label': '¿Cuál es nivel de estudios más alto que terminaste?',
    			'hint': 'education',
    			'type': 'radio',
    			'required': True,
    			'options': Form.Education.choices
    		},
    		{
    			'label': '¿A que escuela fuiste más años?',
    			'hint': 'school',
    			'type': 'radio',
    			'required': True,
    			'options': Form.School.choices
    		},
    		{
    			'label': '¿A que edad aprendiste LSU?',
    			'hint': 'age_of_acquisition',
    			'type': 'radio',
    			'required': True,
    			'options': Form.AgeofAcquisition.choices
    		},
    		{
    			'label': '¿Del 1 al 7, cómo puntuas tu fluidez con la LSU?',
    			'hint': 'lsu_fluency',
    			'type': 'likert',
    			'required': True
    		},
    		{
    			'label': '¿Cuál es tu lengua preferida para comunicarte?',
    			'hint': 'preferred_language',
    			'type': 'radio',
    			'required': True,
    			'options': Form.PreferredLanguage.choices
    		},
    		{
    			'label': '¿En que lengua te comunicas más en tu casa?',
    			'hint': 'language_at_home',
    			'type': 'radio',
    			'required': True,
    			'options': Form.Language.choices
    		}
    	],
    	'hints': {
    		'welcome': static('hints/bienvenida.mp4'),
    		'consent': static('hints/consentimiento.mp4'),
    		'instructions': static('hints/instrucciones.mp4'),
    		'intro': static('hints/intro.mp4'),
    		'name': static('hints/name.mp4'),
    		'contact': static('hints/contact.mp4'),
    		'sex': static('hints/sex.mp4'),
    		'birthdate': static('hints/birthdate.mp4'),
    		'birthplace': static('hints/birthplace.mp4'),
    		'deaf_community': static('hints/deaf_community.mp4'),
    		'ethnicity': static('hints/ethnicity.mp4'),
    		'education': static('hints/education.mp4'),
    		'school': static('hints/school.mp4'),
    		'age_of_acquisition': static('hints/age_of_acquisition.mp4'),
    		'language_at_home': static('hints/language_at_home.mp4'),
    		'preferred_language': static('hints/preferred_language.mp4'),
    		'lsu_fluency': static('hints/lsu_fluency.mp4')
    	},
    	'stimuli': {static('terms/' + stimulus.file_name): stimulus.file_name for stimulus in Stimulus.objects.all()
    	},
    	'mode': mode,
    	'modes': Form.Mode,
    	'timeout': options.online_timeout if mode == Form.Mode.ONLINE else options.offline_timeout if mode == Form.Mode.OFFLINE else options.debug_timeout,
    	'sample_size': options.online_sample_size if mode == Form.Mode.ONLINE else options.offline_sample_size if mode == Form.Mode.OFFLINE else options.debug_sample_size
	}
	return HttpResponse(template.render(context, request))