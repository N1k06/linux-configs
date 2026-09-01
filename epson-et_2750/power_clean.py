#!/usr/bin/env python3
"""
Lancia un Power Cleaning sulla stampante Epson ET-2750 (o altro modello
supportato da epson_print_conf) via LPR, senza passare dalla GUI Tkinter.

Da eseguire nella stessa cartella del repo epson_print_conf, con il venv
attivo (le dipendenze pysnmp/pysnmp_sync_adapter servono solo per la lettura
via SNMP fatta da epson_print_conf.py, non per questo script in sé, ma
l'import della classe Printer richiede comunque il modulo importabile).

Uso:
    python3 power_clean.py -a 192.168.1.110 -m ET-2750
    python3 power_clean.py -a 192.168.1.110 -m ET-2750 --group 1   # solo colore
    python3 power_clean.py -a 192.168.1.110 -m ET-2750 --dry-run
"""

import argparse
import sys

# Import diretto dal modulo del progetto epson_print_conf.
# Deve essere eseguito dalla cartella del repo (o con quella cartella nel PYTHONPATH).
try:
    from epson_print_conf import Printer
except ImportError:
    print(
        "Errore: impossibile importare 'Printer' da epson_print_conf.py.\n"
        "Esegui questo script dalla cartella del repo epson_print_conf, "
        "con il venv attivo.",
        file=sys.stderr,
    )
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Power Cleaning ugelli Epson via LPR (bypass GUI)."
    )
    parser.add_argument(
        "-a", "--address", required=True, help="IP della stampante (es. 192.168.1.110)"
    )
    parser.add_argument(
        "-m", "--model", required=True, help="Modello stampante (es. ET-2750)"
    )
    parser.add_argument(
        "--group",
        type=int,
        default=0,
        help="Gruppo ugelli: 0 = tutti/nero+colore, 1 = solo colore "
        "(dipende dal modello, verificare con check_nozzles se incerti). Default: 0.",
    )
    parser.add_argument(
        "--standard",
        action="store_true",
        help="Esegue una pulizia STANDARD invece di Power Clean "
        "(equivalente al Clean Nozzles normale).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Genera il comando ma non lo invia realmente alla stampante.",
    )
    args = parser.parse_args()

    power_clean = not args.standard

    print(f"Modello: {args.model}")
    print(f"Indirizzo: {args.address}")
    print(f"Gruppo ugelli: {args.group}")
    print(f"Modalità: {'Power Clean' if power_clean else 'Standard Clean'}")

    printer = Printer(model=args.model, hostname=args.address)

    if args.dry_run:
        print("\n[DRY RUN] Nessun comando inviato alla stampante.")
        return

    confirm = input(
        "\nConfermi l'invio del comando di pulizia alla stampante? "
        "Consuma inchiostro e riempie il contatore waste ink. [s/N] "
    )
    if confirm.strip().lower() not in ("s", "si", "sì", "y", "yes"):
        print("Annullato.")
        return

    result = printer.clean_nozzles(args.group, power_clean=power_clean)
    print("\nComando inviato.")
    print(f"Risultato: {result}")
    print(
        "\nSuggerimento: attendi il completamento del ciclo (spia di alimentazione "
        "lampeggiante), poi esegui un controllo ugelli per verificare l'esito."
    )


if __name__ == "__main__":
    main()
