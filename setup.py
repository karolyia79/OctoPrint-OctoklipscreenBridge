# coding=utf-8

from setuptools import setup

plugin_identifier = "octoklipscreen"
plugin_package = "octoprint_octoklipscreen"
plugin_name = "OctoPrint Octoklipscreen Bridge"
plugin_version = "0.4.0"
plugin_description = "Bridge to send serial logs via MQTT to CYD display"
plugin_author = "Károlyi András"
plugin_license = "AGPLv3"

plugin_requires = [
    "paho-mqtt>=1.5.0,<2.0"
]

plugin_additional_data = []

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    license=plugin_license,
    packages=[plugin_package],
    include_package_data=True,
    install_requires=plugin_requires,
    entry_points="""
    [octoprint.plugin]
    {identifier} = {package}
    """.format(identifier=plugin_identifier, package=plugin_package)
)
