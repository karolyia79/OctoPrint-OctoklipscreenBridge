# coding=utf-8
from __future__ import absolute_import

__plugin_name__ = "Octoklipscreen Bridge"
__plugin_version__ = "0.1.0"
__plugin_description__ = "Bridges raw terminal and serial logs to the Octoklipscreen ESP32 display."
__plugin_author__ = "Andras"
__plugin_pythoncompat__ = ">=3,<4"

import octoprint.plugin
import paho.mqtt.client as mqtt

class OctoklipscreenBridgePlugin(octoprint.plugin.StartupPlugin,
                                  octoprint.plugin.SettingsPlugin,
                                  octoprint.plugin.TemplatePlugin):

    def __init__(self):
        self.mqtt_client = None

    def initialize(self):
        self._logger.info("Octoklipscreen Bridge initialized!")
        self._init_mqtt()

    def _init_mqtt(self):
        broker_ip = self._settings.get(["mqtt_broker"])
        mqtt_user = self._settings.get(["mqtt_user"])
        mqtt_pass = self._settings.get(["mqtt_pass"])
        
        if broker_ip:
            try:
                if self.mqtt_client:
                    try:
                        self.mqtt_client.loop_stop()
                        self.mqtt_client.disconnect()
                    except:
                        pass
                
                try:
                    self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "OctoPrint_OctoklipscreenBridge")
                except AttributeError:
                    self.mqtt_client = mqtt.Client("OctoPrint_OctoklipscreenBridge")

                if mqtt_user and mqtt_pass:
                    self.mqtt_client.username_pw_set(mqtt_user, mqtt_pass)

                self.mqtt_client.connect(broker_ip, 1883, 60)
                self.mqtt_client.loop_start()
                self._logger.info("Connected to MQTT broker at {}".format(broker_ip))
            except Exception as e:
                self._logger.error("Failed to connect to MQTT broker: {}".format(e))

    def get_settings_defaults(self):
        return dict(
            mqtt_broker="192.168.1.100",
            mqtt_user="",
            mqtt_pass=""
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def process_serial(self, comm_instance, line, *args, **kwargs):
        if line:
            if self.mqtt_client:
                try:
                    self.mqtt_client.publish("octoklipscreen/terminal", line)
                except Exception as e:
                    self._logger.error("MQTT publish error: {}".format(e))
        return line

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self._init_mqtt()

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = OctoklipscreenBridgePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.received": __plugin_implementation__.process_serial
    }
