from setuptools import setup

plugin_identifier = "octoklipscreen_bridge"
plugin_package = "octoprint_octoklipscreen_bridge"
plugin_name = "OctoPrint-OctoklipscreenBridge"
plugin_version = "0.1.0"
plugin_description = "Bridges raw terminal and serial logs to the Octoklipscreen ESP32 display."
plugin_author = "Andras"

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    packages=[plugin_package],
    include_package_data=True,
    zip_safe=False,
    install_requires=["paho-mqtt>=2.0.0"],
    entry_points="""
        [octoprint.plugin]
        %s = %s
    """ % (plugin_identifier, plugin_package)
)
