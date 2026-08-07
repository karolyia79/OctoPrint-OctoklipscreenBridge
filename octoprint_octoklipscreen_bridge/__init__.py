# coding=utf-8
from __future__ import absolute_import

__plugin_name__ = "Octoklipscreen Bridge"
__plugin_version__ = "0.2.1"
__plugin_description__ = "Bridges OctoPrint log/terminal to MQTT for CYD displays."
__plugin_pythoncompat__ = ">=3,<4"

import octoprint.plugin
import paho.mqtt.client as mqtt
import logging

class OctoklipscreenBridgePlugin(octoprint.plugin.StartupPlugin,
                                  octoprint.plugin.SettingsPlugin,
                                  octoprint.plugin.TemplatePlugin):

    def __init__(self):
        self.mqtt_client = None

    def on_after_startup(self):
        self._init_mqtt()

    def _init_mqtt(self):
        broker_ip = self._settings.get(["mqtt_broker"]) or "localhost"
        mqtt_user = self._settings.get(["mqtt_user"])
        mqtt_pass = self._settings.get(["mqtt_pass"])
        
        try:
            try:
                self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "OctoPrint_Bridge")
            except AttributeError:
                self.mqtt_client = mqtt.Client("OctoPrint_Bridge")

            if mqtt_user and mqtt_pass:
                self.mqtt_client.username_pw_set(mqtt_user, mqtt_pass)
            
            self.mqtt_client.connect(broker_ip, 1883, 60)
            self.mqtt_client.loop_start()
            self._logger.info("Connected to MQTT at {}".format(broker_ip))
        except Exception as e:
            self._logger.error("MQTT Connection Error: {}".format(e))

    def publish_log(self, log_entry):
        if self.mqtt_client and log_entry:
            try:
                # Elküldjük a log üzenetet az MQTT-re
                self.mqtt_client.publish("octoklipscreen/terminal", str(log_entry))
            except Exception:
                pass

    def get_settings_defaults(self):
        return dict(mqtt_broker="localhost", mqtt_user="mosquitto", mqtt_pass="")

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False, template="octoklipscreen_bridge_settings.jinja2")]

# Létrehozunk egy egyedi logging handler-t, ami rákötődik az OctoPrint kommunikációs logjára
class MQTTLogHandler(logging.Handler):
    def __init__(self, plugin_instance):
        logging.Handler.__init__(self)
        self.plugin_instance = plugin_instance

    def emit(self, record):
        try:
            msg = self.format(record)
            # Ha a kommunikációs logból jön a sor, továbbítjuk
            if "octoprint.communication" in record.name:
                self.plugin_instance.publish_log(msg)
        except Exception:
            pass

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = OctoklipscreenBridgePlugin()

    # Rákötjük a handlert az OctoPrint loggolási rendszerére
    root_logger = logging.getLogger("octoprint.communication")
    handler = MQTTLogHandler(__plugin_implementation__)
    root_logger.addHandler(handler)

    global __plugin_hooks__
    __plugin_hooks__ = {}
