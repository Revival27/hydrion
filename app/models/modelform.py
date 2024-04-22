from django.forms import ModelForm
from app.models.hydrosurvey import HydroSurvey

class HydroSurveyForm(ModelForm):
    class Meta:
        model = HydroSurvey
        fields = ['deadline', 'status', 'water_surface', 'location', 'flow_direction', 'flow_direction_speed', 'segment_width', 'segment_depth', 'estimated_waterflow', 'estimated_energy_production']
        #fields = ["Határidő", "Státusz", "Vízfelület", "Áramlás iránya", "Áramlás mért sebessége", "Szelvény szélessége", "Szelvény mélysége", "Becsült vízhozam", "Becsült energia termelés" ]
