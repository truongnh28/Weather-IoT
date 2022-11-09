from django.forms import ModelForm, TextInput, ModelChoiceField

from weather.models import City, Unit, Language


class CityForm(ModelForm):
    language = ModelChoiceField(queryset=Language.objects.all(), empty_label=None)
    unit = ModelChoiceField(queryset=Unit.objects.all(), empty_label=None)

    class Meta:
        model = City
        fields = ['name', 'unit', 'language']
        widgets = {
            'name': TextInput(attrs={
                'class': 'input',
                'placeholder': 'e.g London'
            }),
        }
