# coding=utf-8
from __future__ import absolute_import

__plugin_name__ = "Octoklipscreen Bridge"
__plugin_version__ = "0.1.2"
__plugin_description__ = "Bridges the entire OctoPrint terminal (send and receive) to MQTT for the Octoklipscreen display."
__plugin_author__ = "Karolyi Andras"
__plugin_pythoncompat__ = ">=3,<4"

import octoprint.plugin
import paho.mqtt.client as mqtt

class OctoklipscreenBridgePlugin(octoprint.plugin.StartupPlugin,
                                  octoprint.plugin.SettingsPlugin,
                                  octoprint.plugin.TemplatePlugin):

    def __init__(self):
        self.mqtt_client = None

    def on_after_startup(self):
        self._logger.info("Octoklipscreen Bridge started up, initializing MQTT...")
        self._init_mqtt()

    def _init_mqtt(self):
        broker_ip = self._settings.get(["mqtt_broker"])
        mqtt_user = self._settings.get(["mqtt_user"])
        mqtt_pass = self._settings.get(["mqtt_pass"])
        
        self._logger.info("Configured MQTT Broker IP: {}".format(broker_ip))

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
                self._logger.info("Successfully connected to MQTT broker at {}".format(broker_ip))
            except Exception as e:
                self._logger.error("Failed to connect to MQTT broker: {}".format(e))
        else:
            self._logger.warning("No MQTT broker IP configured!")

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

    def process_sending(self, comm_instance, phase, cmd, parameters, *args, **kwargs):
        line = cmd if not parameters else "{} {}".format(cmd, parameters)
        if line and self.mqtt_client:
            try:
                self.mqtt_client.publish("octoklipscreen/terminal", "Send: " + line)
            except Exception as e:
                self._logger.error("MQTT publish error (send): {}".format(e))
        return None

    def process_received(self, comm_instance, line, *args, **kwargs):
        if line and self.mqtt_client:
            try:
                self.mqtt_client.publish("octoklipscreen/terminal", "Recv: " + line)
            except Exception as e:
                self._logger.error("MQTT publish error (recv): {}".format(e))
        return line

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self._init_mqtt()

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = OctoklipscreenBridgePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.sending": __plugin_implementation__.process_sending,
        "octoprint.comm.protocol.received": __plugin_implementation__.process_received
    }
