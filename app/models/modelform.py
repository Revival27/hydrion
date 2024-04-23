from django import forms
from django.forms import ModelForm
from app.models.hydrosurvey import HydroSurvey


class DateInput(forms.DateInput):
    input_type = 'date'


class HydroSurveyForm(ModelForm):
    class Meta:
        model = HydroSurvey
        fields = ['deadline', 'status', 'water_surface', 'location', 'flow_direction', 'flow_direction_speed', 'segment_width', 'segment_depth', 'estimated_waterflow', 'estimated_energy_production']
        widgets = {
            'deadline': DateInput(),
        }