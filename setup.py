# coding=utf-8

"""
OctoPrint plugin setup configuration with improved compatibility and error handling.
Requires Python 3.7+ and OctoPrint 1.4.0+
"""

import sys
import os

# Verzió-ellenőrzés
if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 7):
    sys.exit(
        "ERROR: OctoklipscreenBridge requires Python 3.7 or higher.\n"
        f"You are using Python {sys.version_info[0]}.{sys.version_info[1]}.\n"
        "Please activate the OctoPrint virtual environment:\n"
        "  source ~/oprint/bin/activate"
    )

# Plugin metadata
plugin_identifier = "octoklipscreen_bridge"
plugin_package = "octoklipscreen_bridge"
plugin_name = "Octoklipscreen Bridge"
plugin_version = "0.4.3"
plugin_description = "Bridge to send serial logs via MQTT to CYD display"
plugin_author = "Károlyi András"
plugin_author_email = ""
plugin_url = "https://github.com/karolyia79/OctoklipscreenBridge"
plugin_license = "AGPLv3"

# Függőségek
plugin_requires = [
    "paho-mqtt>=1.5.0,<3.0"
]

# Adatok és csomagok
plugin_additional_data = ["templates"]
plugin_additional_packages = []
plugin_ignored_packages = []

# Extra setup paraméterek
additional_setup_parameters = {
    "python_requires": ">=3.7,<4",
    "classifiers": [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ]
}

# OctoPrint setuptools import
def import_octoprint_setuptools():
    """
    Import OctoPrint setuptools with informative error handling.
    """
    try:
        import octoprint_setuptools
        return octoprint_setuptools
    except ImportError as e:
        print("\n" + "="*70)
        print("ERROR: Could not import OctoPrint's setuptools module")
        print("="*70)
        print("\nThis error occurs when:")
        print("  1. OctoPrint is not installed")
        print("  2. The OctoPrint virtual environment is not activated")
        print("  3. You're using the wrong Python interpreter")
        print("\nSOLUTION:")
        print("-" * 70)
        print("Make sure you are in the OctoPrint virtual environment:\n")
        print("  source ~/oprint/bin/activate\n")
        print("Then reinstall the plugin:\n")
        print("  pip install -e .\n")
        print("Or for troubleshooting, check Python paths:")
        print(f"  Current Python: {sys.executable}")
        print(f"  Python version: {sys.version}")
        print("\nFull error details:")
        print(f"  {e}")
        print("="*70 + "\n")
        sys.exit(1)

# Import és konfigurálás
octoprint_setuptools = import_octoprint_setuptools()

try:
    from setuptools import setup
except ImportError:
    print("ERROR: setuptools is not installed!")
    print("Please install setuptools: pip install --upgrade setuptools")
    sys.exit(1)

# Setup paraméterek összeállítása
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

# Extra paraméterek hozzáadása
if additional_setup_parameters:
    try:
        from octoprint.util import dict_merge
        setup_parameters = dict_merge(setup_parameters, additional_setup_parameters)
    except ImportError:
        # Fallback: manual merge ha dict_merge nem elérhető
        setup_parameters.update(additional_setup_parameters)

# Setup futtatása
if __name__ == "__main__":
    setup(**setup_parameters)
