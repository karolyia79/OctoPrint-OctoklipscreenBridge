#!/bin/bash

# OctoklipscreenBridge Diagnostic Script
# Segít az Octoprint és MQTT kapcsolódási problémáinak azonosításában

set -e

echo "=========================================="
echo "OctoklipscreenBridge Diagnostic Tool"
echo "=========================================="
echo ""

# Szín definíciók
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Segédfunkciók
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_ok() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 1. Python Verzió Ellenőrzése
print_header "1. Python Verzió Ellenőrzés"
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Telepített verzió: $PYTHON_VERSION"

PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
    print_ok "Python verzió kompatibilis (3.7+)"
else
    print_error "Python verzió túl régi (szükséges: 3.7+)"
fi
echo ""

# 2. OctoPrint Virtual Environment
print_header "2. OctoPrint Virtual Environment"
if [ -d ~/oprint ]; then
    print_ok "Virtual environment könyvtár található: ~/oprint"
    
    if [ -f ~/oprint/bin/python ]; then
        print_ok "Python executable megtalálható"
        VENV_PYTHON=$(~/oprint/bin/python --version 2>&1)
        echo "Virtual environment Python: $VENV_PYTHON"
    else
        print_error "Python executable nem található az virtual environmentben"
    fi
else
    print_warning "Virtual environment könyvtár nem található: ~/oprint"
    echo "Tipikus helyek: ~/oprint, ~/.venv, ~/venv"
fi
echo ""

# 3. OctoPrint Telepítés
print_header "3. OctoPrint Telepítés Ellenőrzése"
if source ~/oprint/bin/activate 2>/dev/null; then
    print_ok "Virtual environment aktiválható"
    
    if python -c "import octoprint" 2>/dev/null; then
        OCTOPRINT_VERSION=$(python -c "import octoprint; print(octoprint.__version__)" 2>/dev/null)
        print_ok "OctoPrint telepítve: verzió $OCTOPRINT_VERSION"
    else
        print_error "OctoPrint nem telepítve"
    fi
    
    if python -c "import octoprint_setuptools" 2>/dev/null; then
        print_ok "octoprint_setuptools elérhető"
    else
        print_error "octoprint_setuptools nem elérhető"
    fi
else
    print_error "Virtual environment nem aktiválható"
fi
echo ""

# 4. paho-mqtt Telepítés
print_header "4. paho-mqtt Függőség"
source ~/oprint/bin/activate 2>/dev/null || true
if python -c "import paho.mqtt" 2>/dev/null; then
    MQTT_VERSION=$(python -c "import paho.mqtt; print(paho.mqtt.__version__)" 2>/dev/null)
    print_ok "paho-mqtt telepítve: verzió $MQTT_VERSION"
else
    print_warning "paho-mqtt nincs telepítve"
    echo "Telepítéshez: pip install 'paho-mqtt>=1.5.0,<3.0'"
fi
echo ""

# 5. OctoPrint Szolgáltatás
print_header "5. OctoPrint Szolgáltatás"
if systemctl is-active --quiet octoprint; then
    print_ok "OctoPrint szolgáltatás fut"
else
    print_error "OctoPrint szolgáltatás nem fut"
    echo "Indítás: sudo systemctl start octoprint"
fi
echo ""

# 6. OctoPrint Log
print_header "6. OctoPrint Naplófájl Ellenőrzése"
LOG_FILE=~/.octoprint/logs/octoprint.log
if [ -f "$LOG_FILE" ]; then
    print_ok "Naplófájl megtalálható: $LOG_FILE"
    echo ""
    echo "Utolsó 20 hiba/figyelmeztetés:"
    grep -i "error\|warning\|exception" "$LOG_FILE" | tail -20 || echo "Nincsenek hibák"
else
    print_warning "Naplófájl nem található: $LOG_FILE"
fi
echo ""

# 7. Serial Logging Ellenőrzése
print_header "7. Serial Logging Ellenőrzése"
SERIAL_LOG=~/.octoprint/logs/serial.log
if [ -f "$SERIAL_LOG" ]; then
    print_ok "Serial log file megtalálható"
    SIZE=$(wc -c < "$SERIAL_LOG")
    echo "Fájl mérete: $SIZE bytes"
    
    if [ "$SIZE" -eq 0 ]; then
        print_warning "Serial log üres - printer csatlakozva?"
    fi
else
    print_warning "Serial log file nem létezik"
    echo "Engedélyezéshez: OctoPrint Settings → Features → Log communication to serial.log"
fi
echo ""

# 8. MQTT Broker Ellenőrzése
print_header "8. MQTT Broker Ellenőrzése"
if command -v mosquitto_sub &> /dev/null; then
    print_ok "mosquitto-clients telepítve"
    
    # Localhost tesztelése
    if nc -zv localhost 1883 &>/dev/null; then
        print_ok "MQTT broker fut a localhost:1883"
        
        # Teszt üzenet
        if mosquitto_pub -h localhost -t "test" -m "test" &>/dev/null 2>&1; then
            print_ok "MQTT közzététel sikeres"
        else
            print_warning "MQTT közzététel sikertelen (authentikáció szükséges?)"
        fi
    else
        print_error "MQTT broker nem fut a localhost:1883"
        echo "Ellenőrzés: sudo systemctl status mosquitto"
    fi
else
    print_warning "mosquitto-clients nincs telepítve"
    echo "Telepítéshez: sudo apt install mosquitto-clients"
fi
echo ""

# 9. Firewall/Port Ellenőrzése
print_header "9. Port Ellenőrzése"
echo "Nyitott portok:"
netstat -tuln 2>/dev/null | grep -E ":(1883|5000)" || echo "netstat nem elérhető"
echo ""

# 10. OctoklipscreenBridge Plugin
print_header "10. OctoklipscreenBridge Plugin Ellenőrzése"
PLUGIN_DIR=~/.octoprint/plugins/octoklipscreen_bridge
if [ -d "$PLUGIN_DIR" ]; then
    print_ok "Plugin könyvtár megtalálható: $PLUGIN_DIR"
    
    if [ -f "$PLUGIN_DIR/__init__.py" ]; then
        print_ok "__init__.py megtalálható"
    else
        print_error "__init__.py nem található"
    fi
else
    print_warning "Plugin könyvtár nem található"
    echo "Plugin telepítéshez: pip install -e /path/to/OctoklipscreenBridge"
fi
echo ""

# 11. Python Szintaxis Ellenőrzése
print_header "11. Python Szintaxis Ellenőrzése"
source ~/oprint/bin/activate 2>/dev/null || true
if [ -f setup.py ]; then
    if python -m py_compile setup.py 2>/dev/null; then
        print_ok "setup.py szintaxis helyes"
    else
        print_error "setup.py szintaxis hiba"
    fi
else
    print_warning "setup.py nem található"
fi
echo ""

# 12. Rendszerirodalom Tömeg
print_header "12. Rendszer Információ"
echo "Operációs rendszer: $(uname -s)"
echo "Operációs rendszer verzió: $(uname -r)"
echo "Hostnév: $(hostname)"
echo "Felhasználó: $(whoami)"
echo ""

# Összegzés
print_header "Diagnózis Összegzés"
echo ""
echo "Javaslatok:"
echo "1. Ha az OctoPrint nincs telepítve, telepítsd: OctoPi image vagy pip install octoprint"
echo "2. Ha paho-mqtt hiányzik: pip install 'paho-mqtt>=1.5.0,<3.0'"
echo "3. Ha MQTT broker nem fut: sudo systemctl restart mosquitto"
echo "4. Ha serial.log üres: engedélyezd a serial logging-ot az OctoPrint Settings-ben"
echo "5. Ha plugin nem működik: sudo systemctl restart octoprint"
echo ""

echo -e "${GREEN}Diagnózis befejezve.${NC}"
echo "Teljes naplók: tail -100 ~/.octoprint/logs/octoprint.log"
