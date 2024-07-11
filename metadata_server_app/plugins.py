import textwrap
import pluggy
from django.http import HttpResponse
from .models import Metadata

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

def download_readme(request, metadata_id):
    try:
        metadata = Metadata.objects.get(id=metadata_id)
        pm = get_plugin_manager()
        readme_content = pm.hook.generate_readme(metadata=metadata)[0]
        response = HttpResponse(readme_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="README_{metadata_id}.txt"'
        return response
    except Metadata.DoesNotExist:
        return HttpResponse("Metadata not found", status=404)