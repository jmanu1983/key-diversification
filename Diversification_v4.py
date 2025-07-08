"""
AES/CMAC Key Diversification Tool

Computes a diversified key from a master key (EMK) using AES-CMAC as specified
in NXP AN10922 (MIFARE DESFire key diversification). Provides a simple tkinter
GUI for interactive use.

Usage:
    python diversification.py

Dependencies:
    pip install pycryptodome
"""

import logging
import os

from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diversification.log")
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def diversify_key(master_key_hex: str, diversification_data_hex: str) -> str:
    """
    Compute a diversified AES-128 key using CMAC.

    Args:
        master_key_hex: 32-char hex string representing the 128-bit master key.
        diversification_data_hex: Hex string of the diversification input
            (UID + APPID_DYNAMIC + FIX).

    Returns:
        32-char hex string of the diversified key.

    Raises:
        ValueError: If inputs are not valid hexadecimal strings.
    """
    key_bytes = bytes.fromhex(master_key_hex)
    div_bytes = bytes.fromhex(diversification_data_hex)

    # Prepend the constant 0x01 as per AN10922
    data = b"\x01" + div_bytes

    # Apply CMAC padding (0x80 followed by 0x00 bytes up to 32 bytes)
    if len(data) < 32:
        data += b"\x80"
        data += b"\x00" * (31 - len(data))

    # Compute AES-CMAC
    cobj = CMAC.new(key_bytes, ciphermod=AES)
    cobj.update(data)
    return cobj.digest().hex().upper()


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

def main():
    """Launch the tkinter GUI."""
    root = Tk()
    root.title("AES/CMAC Key Diversification")
    root.resizable(False, False)

    labels = ["UID", "APPID_DYNAMIC", "FIX", "EMK (Master Key)"]
    entries = {}

    for idx, label_text in enumerate(labels):
        Label(root, text=label_text, anchor="e", width=20).grid(
            row=idx, column=0, padx=6, pady=4, sticky="e"
        )
        entry = Entry(root, width=40)
        entry.grid(row=idx, column=1, padx=6, pady=4)
        entries[label_text] = entry

    result_var = StringVar()
    result_entry = Entry(root, textvariable=result_var, width=40, state="readonly")
    result_entry.grid(row=len(labels) + 1, column=0, columnspan=2, padx=6, pady=4)

    status_label = Label(root, text="", fg="red")
    status_label.grid(row=len(labels) + 2, column=0, columnspan=2)

    def on_diversify():
        uid = entries["UID"].get().strip()
        appid = entries["APPID_DYNAMIC"].get().strip()
        fix = entries["FIX"].get().strip()
        emk = entries["EMK (Master Key)"].get().strip()

        if not all([uid, appid, fix, emk]):
            status_label.config(text="All fields are required.")
            return

        try:
            div_data = uid + appid + fix
            result = diversify_key(emk, div_data)
            result_var.set(result)
            status_label.config(text="", fg="red")
            logger.info("Diversified key: %s", result)
        except Exception as exc:
            logger.error("Diversification failed: %s", exc)
            status_label.config(text=f"Error: {exc}")
            result_var.set("")

    Button(root, text="Diversify", command=on_diversify, width=20).grid(
        row=len(labels), column=0, columnspan=2, pady=8
    )

    root.mainloop()


if __name__ == "__main__":
    main()
