# coding=utf-8
from __future__ import absolute_import
import threading
import time
import os
import paho.mqtt.client as mqtt
import octoprint.plugin

class OctoklipscreenBridgePlugin(octoprint.plugin.StartupPlugin,
                                 octoprint.plugin.SettingsPlugin,
                                 octoprint.plugin.TemplatePlugin):

    def __init__(self):
        self.mqtt_client = None
        self.stop_thread = False
        self.thread = None

    def on_after_startup(self):
        self._init_mqtt()
        self.log_path = os.path.expanduser("~/.octoprint/logs/serial.log")

        self.thread = threading.Thread(target=self._tail_log)
        self.thread.daemon = True
        self.thread.start()

    def _init_mqtt(self):
        broker = self._settings.get(["mqtt_broker"]) or "localhost"
        try:
            # Kompatibilis a 1.x paho-mqtt verziókkal (1.6.1)
            self.mqtt_client = mqtt.Client("OctoPrint_LogBridge")
            user = self._settings.get(["mqtt_user"])
            pwd = self._settings.get(["mqtt_pass"])
            if user:
                self.mqtt_client.username_pw_set(user, pwd)
            self.mqtt_client.connect(broker, 1883, 60)
            self.mqtt_client.loop_start()
            self._logger.info("Octoklipscreen Bridge connected to MQTT.")
        except Exception as e:
            self._logger.error("MQTT connection failed: {}".format(e))

    def _tail_log(self):
        while not os.path.exists(self.log_path) and not self.stop_thread:
            time.sleep(1)
            
        while not self.stop_thread:
            try:
                with open(self.log_path, "r") as f:
                    inode = os.fstat(f.fileno()).st_ino
                    f.seek(0, os.SEEK_END)
                    
                    while not self.stop_thread:
                        if not os.path.exists(self.log_path):
                            break
                        current_inode = os.stat(self.log_path).st_ino
                        if current_inode != inode:
                            break
                            
                        line = f.readline()
                        if not line:
                            time.sleep(0.1)
                            continue
                            
                        if self.mqtt_client:
                            try:
                                self.mqtt_client.publish("octoklipscreen/terminal", line.strip())
                            except Exception:
                                pass
            except Exception:
                time.sleep(1)

    def on_shutdown(self):
        self.stop_thread = True
        if self.mqtt_client:
            try:
                self.mqtt_client.loop_stop()
                self.mqtt_client.disconnect()
            except Exception:
                pass

    def get_settings_defaults(self):
        return dict(
            mqtt_broker="localhost",
            mqtt_user="mosquitto",
            mqtt_pass=""
        )

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False, template="octoklipscreen_bridge_settings.jinja2")]

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = OctoklipscreenBridgePlugin()
