# coding=utf-8

from setuptools import setup

plugin_identifier = "octoklipscreenbridge"
plugin_package = "octoprint_octoklipscreen_bridge"
plugin_name = "OctoPrint Octoklipscreen Bridge"
plugin_version = "0.4.0"
plugin_description = "Bridge to send serial logs via MQTT to CYD display"
plugin_author = "Károlyi András"
plugin_license = "AGPLv3"

plugin_requires = [
    "paho-mqtt>=1.5.0,<2.0"
]

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    license=plugin_license,
    packages=[plugin_package],
    include_package_data=True,
    install_requires=plugin_requires,
    python_requires=">=3",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)",
        "Programming Language :: Python :: 3",
        "Framework :: OctoPrint",
    ],
    entry_points="""
    [octoprint.plugin]
    {identifier} = {package}
    """.format(identifier=plugin_identifier, package=plugin_package)
)
