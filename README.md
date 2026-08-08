# OctoklipscreenBridge - Telepítési és Hibaelhárítási Útmutató

## 📋 Rendszerkövetelmények

- **OctoPrint**: 1.4.0 vagy újabb
- **Python**: 3.7+ (a virális environmentben)
- **MQTT Broker**: Mosquitto vagy bármely MQTT broker
- **Operációs rendszer**: Linux (Raspberry Pi), macOS, vagy Windows

## ✅ Előfeltételek Ellenőrzése

Mielőtt telepítenéd, futtasd ezeket az ellenőrzéseket:

```bash
# 1. OctoPrint virtuális environment aktiválása
source ~/oprint/bin/activate

# 2. Python verzió ellenőrzése
python --version
# Kimenetnek 3.7 vagy újabbnak kell lennie

# 3. OctoPrint telepítés ellenőrzése
pip list | grep octoprint
# OctoPrint-nek kell megjelennie

# 4. pip/setuptools frissítése
pip install --upgrade pip setuptools wheel
```

## 🔧 Normál Telepítés (Ajánlott)

### OctoPrint Web UI-ból

1. **OctoPrint megnyitása** → Menü → Plugin Manager
2. **"Get More" gombra kattintás**
3. **"...from URL" mezőbe beillesztés:**
   ```
   https://github.com/karolyia79/OctoklipscreenBridge/archive/refs/heads/main.zip
   ```
4. **"Install" gombra kattintás**
5. **OctoPrint újraindítása** a Plugin Manager alatt

## 🛠️ Fejlesztői Telepítés

Ha saját módosításokat szeretnél végezni:

```bash
# 1. OctoPrint virtual environment aktiválása
source ~/oprint/bin/activate

# 2. Repository klónozása
mkdir -p ~/octoprint_plugins
cd ~/octoprint_plugins
git clone https://github.com/karolyia79/OctoklipscreenBridge.git
cd OctoklipscreenBridge

# 3. Plugin telepítése szerkesztési módban
pip install -e .

# 4. OctoPrint újraindítása
sudo systemctl restart octoprint

# 5. Naplók megtekintése
tail -f ~/.octoprint/logs/octoprint.log
```

## ⚙️ Konfiguráció

### 1. Serial Logging Bekapcsolása (KÖTELEZŐ!)

Az OctoPrint-ben:
1. **Beállítások (Settings)** → **Features**
2. **Serial Logging** szakasz
3. **✓ Log communication to serial.log** pipálása
4. **Save**

### 2. MQTT Broker Telepítése (Raspberry Pi/Linux)

```bash
# Mosquitto telepítése
sudo apt update
sudo apt install mosquitto mosquitto-clients -y

# Automatikus indítás
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Tesztelés
mosquitto_sub -t "test" &
mosquitto_pub -t "test" -m "Hello"
```

### 3. MQTT Jelszavas Védelem (Ajánlott)

```bash
# Felhasználó létrehozása
sudo mosquitto_passwd -c /etc/mosquitto/passwd mosquitto

# Konfiguráció
sudo nano /etc/mosquitto/conf.d/default.conf
```

Illeszd be:
```
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
```

```bash
# Mosquitto újraindítása
sudo systemctl restart mosquitto
```

### 4. Plugin Beállítása OctoPrint-ben

1. **Beállítások** → **OctoklipscreenBridge**
2. Kitöltsd az MQTT beállításokat:
   - **MQTT Host**: localhost (vagy az MQTT szerver IP-je)
   - **MQTT Port**: 1883
   - **MQTT Username**: mosquitto (vagy a beállított felhasználónév)
   - **MQTT Password**: (a beállított jelszó)
   - **MQTT Topic**: octoprint/serial (vagy egyéni)
3. **Enable MQTT Bridge** pipálása
4. **Save**

## 🐛 Hibaelhárítás

### "Could not import OctoPrint's setuptools"

**Ok:** Az OctoPrint virtual environment nem aktív

**Megoldás:**
```bash
source ~/oprint/bin/activate
pip install -e .
sudo systemctl restart octoprint
```

### "ModuleNotFoundError: No module named 'paho.mqtt'"

**Megoldás:**
```bash
source ~/oprint/bin/activate
pip install paho-mqtt>=1.5.0,<3.0
sudo systemctl restart octoprint
```

### MQTT Csatlakozási Hiba

**Ellenőrizd:**
```bash
# 1. MQTT szerver működik-e?
sudo systemctl status mosquitto

# 2. Port nyitva?
netstat -tuln | grep 1883

# 3. Teszteld a csatlakozást
mosquitto_pub -h localhost -u mosquitto -P jelszó -t "test" -m "test"
```

### A Plugin Nem Jelenik Meg

**Megoldás:**
```bash
# Naplók ellenőrzése
tail -100 ~/.octoprint/logs/octoprint.log

# Plugin könyvtár ellenőrzése
ls -la ~/.octoprint/plugins/

# Újratelepítés
source ~/oprint/bin/activate
pip uninstall octoklipscreen_bridge -y
pip install -e .
sudo systemctl restart octoprint
```

### Serial Log Üres

**Ellenőrzés:**
1. Serial logging **bekapcsolva**-e az OctoPrint Settings-ben?
2. Van-e conectado printer az OctoPrinthez?
3. Ellenőrizd a naplóban: `~/.octoprint/logs/serial.log`

## 📊 MQTT Üzenetek Tesztelése

```bash
# Egy másik terminálból figyeld az üzeneteket
mosquitto_sub -h localhost -u mosquitto -P jelszó -t "octoprint/#" -v

# Vagy grafikus eszközzel (pl. MQTT Explorer):
# https://mqtt-explorer.com/
```

## 📝 MQTT Topic Szerkezet

```
octoprint/
├── serial/      # Soros kommunikáció
├── status/      # Nyomtatási státusz
└── events/      # Nyomtatási események
```

## 🔄 Frissítés

### Automatikus Frissítés

1. **Beállítások** → **Software Update**
2. Ha frissítés elérhető, megjelenik az OctoklipscreenBridge-hez

### Manuális Frissítés

```bash
source ~/oprint/bin/activate
cd ~/octoprint_plugins/OctoklipscreenBridge
git pull
pip install -e .
sudo systemctl restart octoprint
```

## 📋 Naplózás és Debug

### Részletes Naplózás Engedélyezése

1. **Beállítások** → **Logging**
2. Keress az `octoklipscreen_bridge` logger-re
3. Állítsd **DEBUG** szintre
4. **Save**

```bash
# Naplók valós időben
tail -f ~/.octoprint/logs/octoprint.log | grep octoklipscreen
```

### Log Elérési Helyek

```bash
# OctoPrint logs
~/.octoprint/logs/octoprint.log

# Mosquitto logs
tail -f /var/log/mosquitto/mosquitto.log

# System journal (Raspberry Pi)
sudo journalctl -u octoprint -f
```

## 🆘 Támogatás és Problémájelentés

Ha a probléma nem oldódik meg:

1. **GitHub Issues**: https://github.com/karolyia79/OctoklipscreenBridge/issues
2. **OctoPrint Community**: https://community.octoprint.org/
3. **Csatolt információk:**
   - Python verzió: `python --version`
   - OctoPrint verzió: OctoPrint UI → About
   - Naplófájlok: `~/.octoprint/logs/octoprint.log` (utolsó 100 sor)
   - MQTT teszt kimenetele

## 📚 Adapterek és Kompatibilitás

### Támogatott MQTT Brokerek

- ✅ Mosquitto (ajánlott)
- ✅ ActiveMQ
- ✅ RabbitMQ
- ✅ EMQX
- ✅ AWS IoT

### Támogatott Kijelzők

- ✅ CYD (Cheap Yellow Display)
- ✅ ESP32 MQTT kliensek
- ✅ Home Assistant MQTT integrációk

## 💡 Tippek és Trükkök

### Raspberry Pi Erőforrások Takarékossága

```bash
# Mosquitto konfigurálása alacsony memóriához
sudo nano /etc/mosquitto/conf.d/memory.conf

# Illeszd be:
max_connections -1
max_queued_messages 0
```

### Auto-restart OctoklipscreenBridge Hiba után

```bash
# Systemd service fájl létrehozása
sudo nano /etc/systemd/system/octoprint-bridge-watcher.service

# Illeszd be:
[Unit]
Description=OctoklipscreenBridge Watcher
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/python3 -c "import time; time.sleep(10)"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

**Utolsó frissítés:** 2026. augusztus
**Plugin verzió:** 0.4.2+
