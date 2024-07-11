from django import forms
from .models import Metadata

class MetadataForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ['data_provider', 'data_format', 'other_data_format', 'degree_of_aggregation']