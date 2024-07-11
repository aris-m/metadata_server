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