from django import forms
from .models import Metadata

class MetadataForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ['data_provider', 'data_format', 'other_data_format', 'degree_of_aggregation']
        
        def clean(self):
            data_format = self.cleaned_data.get('data_format')
            other_data_format = self.cleaned_data.get('other_data_format')
            if data_format == 'other' and not other_data_format:
                raise forms.ValidationError({'other_data_format': 'This field is required when "other" is selected.'})