# Epson ET-2750 — Reset contatore waste ink + Power Cleaning

Procedura per sbloccare la stampante quando pulizia testina / power cleaning risultano disabilitati dal firmware per contatore waste ink "pieno", e per forzare un power cleaning quando l'ugello giallo (o altri) risultano ostruiti.

**Setup di riferimento:** Arch Linux, Python 3.14, stampante collegata in Wi-Fi.

---

## 0. Prerequisiti hardware (una tantum)

Se i tamponi di scarico interni sono fisicamente saturi, vanno sostituiti o bypassati prima di procedere via software — resettare solo il contatore senza intervenire sui tamponi pieni causa fuoriuscite di inchiostro all'interno della stampante.

- Tamponi interni sostituiti oppure bypassati con tubicino deviato verso un contenitore esterno (es. barattolo di vetro) per raccogliere lo scarico.
- Verificare periodicamente il livello del contenitore esterno, se usato.

## 1. Trovare l'IP della stampante

Dal pannello della stampante: menu Wi-Fi/Rete → Stato rete. Oppure dalla lista dispositivi del router.

Nel nostro caso: `192.168.1.110`

## 2. Setup ambiente Python (una tantum)

```bash
git clone https://github.com/Ircama/epson_print_conf
cd epson_print_conf

python -m venv ~/.venv-epson
source ~/.venv-epson/bin/activate

pip install --upgrade pip
pip install "setuptools<81"
pip install --no-build-isolation -r requirements.txt
```

> Nota: `--no-build-isolation` è necessario perché su Python 3.14 il build isolato di `pysnmp_sync_adapter` non trova `pkg_resources`. Se in futuro il progetto aggiorna le dipendenze, questo passaggio potrebbe non servire più.

### 2.1 Patch per Python 3.14 (bug event loop asyncio)

Su Python 3.14, `epson_print_conf.py` va in errore (`no current event loop in thread 'MainThread'`) a causa della rimozione della creazione implicita dell'event loop asyncio. Bug tracciato su [issue #119](https://github.com/Ircama/epson_print_conf/issues/119), non ancora risolto upstream al momento di questa stesura.

Aprire `epson_print_conf.py` e, subito dopo il blocco di import in cima al file (dopo la riga `from pysnmp.hlapi.v1arch.asyncio import *`), aggiungere:

```python
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
```

> Se in una futura versione del repository questo bug risulta corretto, il fix manuale non è più necessario — verificare prima di riapplicarlo.

### 2.2 Tkinter per la GUI (serve solo per il power cleaning)

```bash
sudo pacman -S tk
```

---

## 3. Riattivare l'ambiente (ogni volta)

```bash
cd ~/epson_print_conf
source ~/.venv-epson/bin/activate
```

Il prompt deve mostrare `(.venv-epson)` all'inizio.

## 4. Verificare lo stato attuale (sempre prima di modificare)

```bash
python3 epson_print_conf.py -m ET-2750 -a 192.168.1.110 -i
```

Controllare in particolare:
- `waste_ink_levels` → `main_waste` e `borderless_waste` (percentuale)
- `maintenance_box_1` / `maintenance_box_2` → `full` o `not full`
- `Maintenance required level ...` → soglia oltre la quale la stampante si blocca

## 5. Reset del contatore waste ink

**Permanente** (azzera i contatori, riscrive l'EEPROM):
```bash
python3 epson_print_conf.py -m ET-2750 -a 192.168.1.110 --reset_waste_ink
```

**Temporaneo** (bypassa il blocco senza toccare l'EEPROM, si annulla al riavvio):
```bash
python3 epson_print_conf.py -m ET-2750 -a 192.168.1.110 --temp_reset_waste_ink
```

> Usare `--reset_waste_ink` solo dopo aver effettivamente sostituito o bypassato i tamponi fisici (vedi punto 0) — il reset rimuove solo il blocco software, non risolve un problema fisico di tamponi saturi.

Aggiungere `--dry-run` a qualsiasi comando di scrittura per simulare l'operazione senza eseguirla davvero.

## 6. Power Cleaning

Il progetto `epson_print_conf` non espone il power cleaning come flag dedicato nella CLI principale (`epson_print_conf.py -h` non lo elenca) — è disponibile "di fabbrica" solo tramite la GUI Tkinter (`ui.py`). Il comando effettivo verso la stampante è lo stesso in entrambi i casi (stessa funzione `clean_nozzles(group, power_clean=True/False)` del modulo `epson_escp2`), cambia solo l'interfaccia usata per richiamarla.

Due opzioni equivalenti:

### 6a. Via GUI (soluzione "di fabbrica" del progetto)

```bash
python3 ui.py -m ET-2750 -a 192.168.1.110
```

Nella finestra: cercare il pulsante **"Power Clean"** (distinto da "Clean Nozzles", che è la pulizia standard).

### 6b. Via script CLI standalone (`power_clean.py`, aggiunto a questo repo)

Per evitare la GUI, `power_clean.py` importa direttamente la classe `Printer` di `epson_print_conf.py` e chiama `clean_nozzles()` da riga di comando.

**Installazione (una tantum):** copiare `power_clean.py` nella cartella del repo, accanto a `epson_print_conf.py` (necessario per l'import):
```bash
cp power_clean.py ~/epson_print_conf/
```

**Utilizzo:**
```bash
cd ~/epson_print_conf
source ~/.venv-epson/bin/activate

# Power cleaning (default), con richiesta di conferma prima dell'invio
python3 power_clean.py -a 192.168.1.110 -m ET-2750

# Solo simulazione, nessun comando inviato alla stampante
python3 power_clean.py -a 192.168.1.110 -m ET-2750 --dry-run

# Pulizia standard invece di power clean
python3 power_clean.py -a 192.168.1.110 -m ET-2750 --standard

# Selezione gruppo ugelli (0 = default/tutti, 1 = solo colore su alcuni modelli)
python3 power_clean.py -a 192.168.1.110 -m ET-2750 --group 1
```

Lo script chiede conferma esplicita (`s`/`N`) prima di inviare davvero il comando, per evitare cicli accidentali.

> **Nota**: lo script è stato scritto basandosi sull'esempio ufficiale nel README di `epson_print_conf` (`self.printer.clean_nozzles(0)`) e sulla firma della funzione nel modulo `epson_escp2`, ma non è stato verificato end-to-end su hardware reale al momento della stesura. Se al primo lancio compare un `ImportError` o `TypeError` sui parametri di `Printer(...)` o `clean_nozzles(...)`, verificare i nomi esatti con:
> ```bash
> grep -n "class Printer\|def clean_nozzles\|def __init__" epson_print_conf.py
> ```
> e correggere lo script di conseguenza.

**Prima di lanciare il power cleaning (con qualsiasi metodo):**
- Verificare che tutti i serbatoi d'inchiostro siano almeno a un terzo pieni.
- Il power cleaning consuma molto più inchiostro della pulizia standard e riempie più rapidamente il contatore waste ink.

**Dopo il power cleaning:**
- Stampare un test ugelli per verificare il risultato.
- Se il problema persiste, attendere almeno 12 ore prima di ripetere un altro power cleaning (indicazione ufficiale Epson) — non incatenare cicli multipli di fila.
- Se dopo alcuni tentativi il problema non migliora, può indicare un'ostruzione fisica dell'ugello non risolvibile via software.

---

## Alternativa: Power Cleaning dal pannello della stampante (senza PC)

Se si vuole evitare il tool per il solo power cleaning (ma serve comunque per sbloccare il contatore se pieno):

1. Sul pannello LCD della stampante, toccare l'icona degli **strumenti di manutenzione** (a seconda del firmware può essere un'icona a forma di chiave inglese, oppure raggiungibile da **Impostazioni**).
2. Selezionare **Manutenzione testina di stampa**.
3. Scegliere **Pulizia approfondita testina** (Power Cleaning) — su alcuni firmware italiani compare come "Pulizia intensiva" o simile.
4. Confermare l'avvio; la spia di alimentazione lampeggia durante il ciclo.
5. Al termine, eseguire dal pannello un **controllo ugelli** (Controllo ugelli testina) per verificare il risultato stampando il pattern di test.
6. Se il pattern mostra ancora righe mancanti o interrotte, spegnere la stampante e attendere almeno 12 ore prima di ripetere.

> Se questa opzione risulta bloccata/disabilitata dal pannello e rimanda al sito Epson con un QR code, significa che il blocco waste ink è ancora attivo: tornare al punto 5 di questo documento per il reset via software prima di riprovare dal pannello.

---

## Riepilogo comandi rapidi

```bash
# Attivazione ambiente
cd ~/epson_print_conf && source ~/.venv-epson/bin/activate

# Stato attuale
python3 epson_print_conf.py -m ET-2750 -a 192.168.1.110 -i

# Reset permanente contatore
python3 epson_print_conf.py -m ET-2750 -a 192.168.1.110 --reset_waste_ink

# Power cleaning via GUI
python3 ui.py -m ET-2750 -a 192.168.1.110

# Power cleaning via script CLI standalone (alternativa alla GUI)
python3 power_clean.py -a 192.168.1.110 -m ET-2750
```