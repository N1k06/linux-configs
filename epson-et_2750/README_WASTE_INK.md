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

## 6. Power Cleaning (via GUI)

Il power cleaning non è disponibile da riga di comando, solo dalla GUI del tool.

```bash
python3 ui.py -m ET-2750 -a 192.168.1.110
```

Nella finestra: cercare il pulsante **"Power Clean"** (distinto da "Clean Nozzles", che è la pulizia standard).

**Prima di lanciarlo:**
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

# GUI per power cleaning
python3 ui.py -m ET-2750 -a 192.168.1.110
```
