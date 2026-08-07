# OctoPrint Octoklipscreen Bridge

Ez az OctoPrint plugin arra szolgál, hogy a nyomtató soros kommunikációs logját háttérszálon elkapva, MQTT-n keresztül továbbítsa szűrés nélkül, soronként, a könnyű feldolgozhatóság érdekében

---

## ⚠️ FONTOS: A "serial.log" BEKAPCSOLÁSA (KÖTELEZŐ!)

Ahhoz, hogy a plugin látja a nyomtatási terminál adatait, az OctoPrintben engedélyezni kell a kommunikációs naplózást. **Enélkül a plugin nem fog adatokat kapni!**

1. Nyisd meg az OctoPrint felületét.
2. Menj a **Beállítások (Settings)** -> **Features** fülre.
3. Keresd meg a **Serial logging** szakaszt.
4. Pipáld be a **`Log communication to serial.log`** opciót. *(Igen, ez az a bizonyos naplózó funkció, amivel eddig szívtunk, de mostantól erre épül a rendszer!)*
5. Mentsd el a beállításokat.

---

## 🛠️ MQTT Broker Telepítése és Beállítása (Raspberry Pi / Linux)

Ha még nincs MQTT broker (Mosquitto) telepítve az OctoPrintet futtató gépre, az alábbi parancsokkal tudod feltenni és beállítani:

### 1. Telepítés
Nyiss egy SSH terminált, és futtasd:
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients -y
```

### 2. Automatikus indítás beállítása
Biztosítsd, hogy a Mosquitto elinduljon a rendszerrel együtt:
```Bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

### 3. Jelszavas védelem beállítása (Ajánlott)
Hozz létre egy felhasználót (pl. mosquitto néven):
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd mosquitto
```
(A parancs után add meg a kívánt jelszót!)

### 4. Mosquitto konfigurálása
Hozz létre vagy szerkeszd a konfig fájlt:
```
sudo nano /etc/mosquitto/conf.d/default.conf
```
Illeszd be az alábbi sorokat:
```
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
```
Majd indítsd újra a Mosquitto szolgáltatást:
```
sudo systemctl restart mosquitto
```
## 📥 Normál telepítés (OctoPrint felületről) - Ajánlott

 1. Másold ki a GitHub repód ZIP archívumának direkt linkjét (https://github.com/karolyia79/octoprint-octoklipscreen/archive/refs/heads/master.zip).
 2. Nyisd meg az OctoPrint felületét, majd menj a Plugin Manager menüpontba.
 3. Kattints a Get More gombra, majd alul a "...from URL" mezőbe illeszd be a linket.
 4. Kattints az Install gombra, majd a telepítés végén indítsd újra az OctoPrintet.


## 📥 Telepítés (Fejlesztői módban)

### 1. Hozd létre a megfelelő könyvtárat, lépj bele, majd klónozd le a GitHub repót:
   ```
   mkdir -p ~/octoprint_dev
   cd ~/octoprint_dev
   git clone [https://github.com/FELHASZNALONEV/octoprint-octoklipscreen.git](https://github.com/FELHASZNALONEV/octoprint-octoklipscreen.git)
   cd octoprint-octoklipscreen
   ```
### 2. Aktiváld az OctoPrint virtuális környezetét::
```
source ~/oprint/bin/activate
```
### 3. Telepítsd a csomagot fejlesztői módban:
```
pip install -e .
```
### 4. Indítsd újra az OctoPrintet:
```
sudo systemctl restart octoprint
```
