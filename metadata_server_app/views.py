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