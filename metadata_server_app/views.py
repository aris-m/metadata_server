from django.shortcuts import render, redirect
from .forms import MetadataForm
from .models import Metadata

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