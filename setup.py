# coding=utf-8

from setuptools import setup

plugin_identifier = "octoklipscreenbridge"
plugin_package = "octoprint_octoklipscreenbridge"
plugin_name = "OctoPrint-OctoklipscreenBridge"
plugin_version = "0.4.0"
plugin_description = "Bridge to send serial logs via MQTT to CYD display"
plugin_author = "Károlyi András"
plugin_author_email = ""
plugin_url = "https://github.com/karolyia79/OctoPrint-OctoklipscreenBridge"
plugin_license = "AGPLv3"

plugin_requires = [
    "paho-mqtt>=1.5.0,<2.0"
]

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    url=plugin_url,
    license=plugin_license,
    packages=[plugin_package],
    include_package_data=True,
    zip_safe=False,
    install_requires=plugin_requires,
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)",
        "Programming Language :: Python :: 3",
        "Framework :: OctoPrint",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Printing",
    ],
    entry_points="""
    [octoprint.plugin]
    {identifier} = {package}
    """.format(identifier=plugin_identifier, package=plugin_package)
)
