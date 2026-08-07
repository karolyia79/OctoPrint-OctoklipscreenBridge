from setuptools import setup

PLUGIN_IDENTIFIER = "octoklipscreen_bridge"
PLUGIN_PACKAGE = "octoprint_octoklipscreen_bridge"
PLUGIN_NAME = "OctoPrint-OctoklipscreenBridge"
PLUGIN_VERSION = "0.1.5"
PLUGIN_DESCRIPTION = "Bridges OctoPrint terminal to MQTT for CYD displays."
PLUGIN_AUTHOR = "Andras Karolyi"
PLUGIN_URL = "https://github.com/karolyia79/OctoPrint-OctoklipscreenBridge"
PLUGIN_LICENSE = "AGPL-3.0"

setup(
    name=PLUGIN_NAME,
    version=PLUGIN_VERSION,
    description=PLUGIN_DESCRIPTION,
    author=PLUGIN_AUTHOR,
    url=PLUGIN_URL,
    license=PLUGIN_LICENSE,
    packages=[PLUGIN_PACKAGE],
    package_data={
        PLUGIN_PACKAGE: ["templates/*.jinja2"],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3,<4",
    install_requires=[],
    entry_points="""
        [octoprint.plugin]
        {0} = {1}
    """.format(PLUGIN_IDENTIFIER, PLUGIN_PACKAGE)
)
