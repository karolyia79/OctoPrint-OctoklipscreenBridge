# coding=utf-8

plugin_identifier = "octoklipscreen_bridge"
plugin_package = "octoklipscreen_bridge"
plugin_name = "Octoklipscreen Bridge"
plugin_version = "0.4.2"
plugin_description = "Bridge to send serial logs via MQTT to CYD display"
plugin_author = "Károlyi András"
plugin_author_email = ""
plugin_url = "https://github.com/karolyia79/OctoklipscreenBridge"
plugin_license = "AGPLv3"

plugin_requires = [
    "paho-mqtt>=1.5.0,<3.0"
]

# Itt csatoljuk be a sablonokat, hogy a wheel építés ne szálljon el
plugin_additional_data = ["templates"]
plugin_additional_packages = []
plugin_ignored_packages = []

additional_setup_parameters = {
    "python_requires": ">=3,<4",
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)",
    ]
}

from setuptools import setup

try:
    import octoprint_setuptools
except:
    print("Could not import OctoPrint's setuptools, are you sure you are running that under "
          "the same python installation that OctoPrint is installed under?")
    import sys
    sys.exit(-1)

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
    identifier=plugin_identifier,
    package=plugin_package,
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    mail=plugin_author_email,
    url=plugin_url,
    license=plugin_license,
    requires=plugin_requires,
    additional_packages=plugin_additional_packages,
    ignored_packages=plugin_ignored_packages,
    additional_data=plugin_additional_data
)

if len(additional_setup_parameters):
    from octoprint.util import dict_merge
    setup_parameters = dict_merge(setup_parameters, additional_setup_parameters)

setup(**setup_parameters)
