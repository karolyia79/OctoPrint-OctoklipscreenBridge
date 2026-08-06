from setuptools import setup

plugin_identifier = "octoklipscreen_bridge"
plugin_package = "octoprint_octoklipscreen_bridge"
plugin_name = "OctoPrint Octoklipscreen Bridge"
plugin_version = "0.1.0"
plugin_description = "Bridges raw terminal and serial logs to the Octoklipscreen ESP32 display."
plugin_author = "Andras"
plugin_url = "https://github.com/karolyia79/OctoPrint-OctoklipscreenBridge"
plugin_license = "AGPLv3"

plugin_requires = ["paho-mqtt>=1.5.0"]

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    url=plugin_url,
    packages=[plugin_package],
    entry_points="""
        [octoprint.plugin]
        {} = {}
    """.format(plugin_identifier, plugin_package),
    install_requires=plugin_requires,
    include_package_data=True
)