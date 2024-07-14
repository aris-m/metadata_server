from django.shortcuts import render, redirect
from .forms import MetadataForm
from .models import Metadata
from django.http import HttpResponse
from .plugins import get_plugin_manager

def insert_metadata(request):
    if request.method == 'POST':
        form = MetadataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insert-metadata')
    else:
        form = MetadataForm()
    return render(request, 'metadata_form.html', {'form': form})

def list_metadata(request):
    metadata_list = Metadata.objects.all()
    return render(request, 'metadata_list.html', {'metadata_list' : metadata_list})

def download_readme(request, metadata_id):
    try:
        metadata = Metadata.objects.get(id=metadata_id)
        pm = get_plugin_manager()
        generated_readme = pm.hook.generate_readme(metadata=metadata)[0]
        return generated_readme
    except Metadata.DoesNotExist:
        return HttpResponse("Metadata not found", status=404)