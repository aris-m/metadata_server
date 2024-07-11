from django.db import models
from django.core.exceptions import ValidationError

class Metadata(models.Model):
    data_format_choices = [
        ('csv', 'csv'),
        ('xlsx', 'xlsx'),
        ('tsv', 'tsv'),
        ('json', 'json'),
        ('xml', 'xml'),
        ('txt', 'txt'),
        ('md', 'md'),
        ('tex', 'tex'),
        ('jpeg', 'jpeg'),
        ('png', 'png'),
        ('zip', 'zip'),
        ('tar', 'tar'),
        ('other', 'other'),
    ]
    
    
    data_provider = models.CharField(max_length=100)
    data_format = models.CharField(max_length=20, choices=data_format_choices)
    other_data_format = models.CharField(max_length=20, blank=True, null=True)
    degree_of_aggregation = models.CharField(max_length=100)
    
    def clean(self):
        if self.data_format == 'other' and not self.other_data_format:
            raise ValidationError({'other_data_format': 'This field is required when "Other" is selected.'})