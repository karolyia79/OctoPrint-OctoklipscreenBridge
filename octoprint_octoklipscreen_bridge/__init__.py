# coding=utf-8
from __future__ import absolute_import

__plugin_name__ = "Octoklipscreen Bridge"
__plugin_version__ = "0.1.7"
__plugin_description__ = "Bridges OctoPrint terminal to MQTT for CYD displays."
__plugin_pythoncompat__ = ">=3,<4"

import octoprint.plugin
import paho.mqtt.client as mqtt

class OctoklipscreenBridgePlugin(octoprint.plugin.StartupPlugin,
                                  octoprint.plugin.SettingsPlugin,
                                  octoprint.plugin.TemplatePlugin):

    def __init__(self):
        self.mqtt_client = None

    def on_after_startup(self):
        self._init_mqtt()
        # Küldjünk egy teszt üzenetet induláskor, hogy lássuk, megy-e az MQTT
        if self.mqtt_client:
            try:
                self.mqtt_client.publish("octoklipscreen/status", "plugin_started")
                self._logger.info("Test message published to octoklipscreen/status")
            except Exception as e:
                self._logger.error("Startup publish error: {}".format(e))

    def _init_mqtt(self):
        broker_ip = self._settings.get(["mqtt_broker"]) or "localhost"
        mqtt_user = self._settings.get(["mqtt_user"])
        mqtt_pass = self._settings.get(["mqtt_pass"])
        
        self._logger.info("Initializing MQTT broker connection to: {}".format(broker_ip))
        try:
            try:
                self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "OctoPrint_Bridge")
            except AttributeError:
                self.mqtt_client = mqtt.Client("OctoPrint_Bridge")

            if mqtt_user and mqtt_pass:
                self.mqtt_client.username_pw_set(mqtt_user, mqtt_pass)
            
            self.mqtt_client.connect(broker_ip, 1883, 60)
            self.mqtt_client.loop_start()
            self._logger.info("Successfully connected to MQTT at {}".format(broker_ip))
        except Exception as e:
            self._logger.error("MQTT Connection Error: {}".format(e))

    def on_received_line(self, comm_instance, line, *args, **kwargs):
        if line:
            self._logger.info("Line received from printer: {}".format(line.strip()))
            if self.mqtt_client:
                try:
                    self.mqtt_client.publish("octoklipscreen/terminal", line.strip())
                except Exception as e:
                    self._logger.error("MQTT Publish Error: {}".format(e))
        return line

    def get_settings_defaults(self):
        return dict(mqtt_broker="localhost", mqtt_user="mosquitto", mqtt_pass="")

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False, template="octoklipscreen_bridge_settings.jinja2")]

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = OctoklipscreenBridgePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.received": __plugin_implementation__.on_received_line
    }
