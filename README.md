# Create python dummy web server with django

## Django initial setup through CLI
1. install django with pip
    - pip install django
2. initialize django project as admin
    - django-admin startproject core .
3. initialize django application with chosen app name (in this case metadata_server_app)
    - python manage.py startapp metadata_server_app
4. add the just created app to the list of known apps in settings.py
   ```python
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'metadata_server_app',
    ]
    ```
5. link project level urls.py to app level urls.py
   ```python
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("", include("metadata_server_app.urls")),
    ]
    ```
        
## Django model to represent the research data metadata as a database entity
```python
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
```
<p>all the fields are set to CharField since the expected input values are middle sized text. In addition to that data_format contains a list of the default known data formats. In the case that the data format is not listed in the list then it can be inserted through the other_data_format field.</p>

## Form class for the metadata input form
```python
from django import forms
from .models import Metadata

class MetadataForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ['data_provider', 'data_format', 'other_data_format', 'degree_of_aggregation']
```
<p>By setting the model to Metadata if the form is filled correctly according to the given constraints then the entry will be saved as a Metadata object</p>

## Migrate the changes
<p>Update the database schema management with migration</p>
- python manage.py makemigrations
- python manage.py migrate

## Views to handle the HTTP requests

### View to insert the Metadata Entry
```python
from django.shortcuts import render, redirect
from .forms import MetadataForm

def insert_metadata(request):
    if request.method == 'POST':
        form = MetadataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insert-metadata')
    else:
        form = MetadataForm()
    return render(request, 'metadata_form.html', {'form': form})
```
<p>This view will return the metadata input form if the HTTP request is a get request. If its post request then the view will check for the validty of the entry and only saves it in the database if the entry is valid and redirect backs to the same page in case the user would like to insert another entry.</p>

### View to show all the metadata entries in the database
```python
from django.shortcuts import render
from .models import Metadata

def list_metadata(request):
    metadata_list = Metadata.objects.all()
    return render(request, 'metadata_list.html', {'metadata_list' : metadata_list})
```
<p>This view finds all objects of Metadata class registered in the database</p>

### App level paths to the views
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_metadata, name='list-metadata'),
    path('insert-metadata/', views.insert_metadata, name='insert-metadata')
]
```

## HTML templates for the web pages

### Metadata form
```html
<!DOCTYPE html>
<html>
<head>
    <title>Research Metadata Form</title>
</head>
<body>
    <h1>Enter Research Metadata</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
    <br>
    <a href="{% url 'list-metadata' %}">Back</a>
</body>
</html>
```
<p>a simple html form page with a submit button to send post request to the insert_metadata view and a button to go back to the metadata list page. CSRF token is included to make sure that the requests are legitimate.</p>

### metadata list html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Research Metadata Form</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 15px;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>Research Data Metadata List</h1>
    <table>
        <thead>
            <tr>
                <th>Data Provider</th>
                <th>Data Format</th>
                <th>Degree of Aggregation</th>
            </tr>
        </thead>
        <tbody>
            {% for metadata in metadata_list %}
            <tr>
                <td>{{ metadata.data_provider }}</td>
                <td>
                    {% if metadata.data_format == 'other' %}
                        {{ metadata.other_data_format }}
                    {% else %}
                        {{ metadata.data_format }}
                    {% endif %}
                </td>
                <td>{{ metadata.degree_of_aggregation }}</td>
                <td><a href="{% url 'download_readme' metadata_id=metadata.id %}">Download README.txt</a></td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4">No entries found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <p><a href="{% url 'insert-metadata' %}">Add New Metadata</a></p>
</body>
</html>
```
<p>The Metadata entries are shown as table entries in this page with an additional option to download the metadata entries as a README file. A button is provided at the bottom of the table to add new entries.</p>

## Plugin to download README file with pluggy
```python
import textwrap
import pluggy

hookspec = pluggy.HookspecMarker("metadata_plugin")
hookimpl = pluggy.HookimplMarker("metadata_plugin")

class MetadataPluginSpec:
    @hookspec
    def generate_readme(self, metadata):
        pass

class MetadataPlugin:
    @hookimpl
    def generate_readme(self, metadata):
        if metadata.data_format == "other":
            format = metadata.other_data_format
        else:
            format = metadata.data_format
            
        dublin_core = textwrap.dedent(f"""
        <meta name="DC.Creator" content="{metadata.data_provider}">
        <meta name="DC.Format" content="{format}">
        <meta name="DC.Description" content="{metadata.degree_of_aggregation}">
        """).strip()
        return dublin_core

def get_plugin_manager():
    pm = pluggy.PluginManager("metadata_plugin")
    pm.add_hookspecs(MetadataPluginSpec)
    pm.register(MetadataPlugin())
    return pm
```
<p>A hook specification that takes in an instance of the Metadata class as parameter is created. In the hook implementation the dublin core schema of the specific Metadata instance will be generated. The content of DC.Format will be changed dyanmically according to the data_format. 
  If the value of data_format is 'others' then DC.Format will be set to the value of the other_data_format field</p>

### Add view and url path to call the plugin
```python
urlpatterns = [
    path('', views.list_metadata, name='list-metadata'),
    path('download_readme/<int:metadata_id>/', views.download_readme, name='download_readme'),
    path('insert-metadata/', views.insert_metadata, name='insert-metadata')
]
```
```python
def download_readme(request, metadata_id):
    try:
        metadata = Metadata.objects.get(id=metadata_id)
        pm = get_plugin_manager()
        readme_content = pm.hook.generate_readme(metadata=metadata)[0]
        response = HttpResponse(readme_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="README_{metadata.data_provider}.txt"'
        return response
    except Metadata.DoesNotExist:
        return HttpResponse("Metadata not found", status=404)
```
<p>This view will call the generate_readme plugin on the chosen metadata object and handle the response as a README file attachment</p>
