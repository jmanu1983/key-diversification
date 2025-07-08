# Key Diversification Tool

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![PyCryptodome](https://img.shields.io/badge/Crypto-AES%2FCMAC-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

An **AES/CMAC key diversification** tool with a tkinter GUI, implementing the NXP AN10922 specification for MIFARE DESFire key diversification. Used in access control systems to derive unique card keys from a master key.

## How It Works

The tool computes a diversified AES-128 key using:

1. **Input**: UID + Application ID + Fixed data + Master Key (EMK)
2. **Process**: Prepends constant `0x01`, applies CMAC padding, computes AES-CMAC
3. **Output**: 128-bit diversified key unique to the card

```
Diversified Key = AES-CMAC(EMK, 0x01 || UID || APPID_DYNAMIC || FIX)
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| Cryptography | PyCryptodome (AES, CMAC) |
| GUI | tkinter |

## Installation

```bash
git clone https://github.com/jmanu1983/key-diversification.git
cd key-diversification

pip install -r requirements.txt
```

## Usage

```bash
python Diversification_v4.py
```

The GUI will open with the following fields:

| Field | Description | Example |
|-------|------------|---------|
| UID | Card unique identifier (hex) | `04A23BC1D52E80` |
| APPID_DYNAMIC | Application ID (hex) | `F54100` |
| FIX | Fixed diversification data (hex) | `4E585020416275` |
| EMK | Encryption Master Key (hex) | `00112233445566778899AABBCCDDEEFF` |

Click **Diversify** to compute the diversified key.

## Project Structure

```
key-diversification/
├── Diversification_v4.py   # Main application (latest version)
├── requirements.txt        # Python dependencies
└── README.md
```

## References

- [NXP AN10922 — AES Key Diversification](https://www.nxp.com/docs/en/application-note/AN10922.pdf)
- [MIFARE DESFire EV1/EV2 documentation](https://www.nxp.com/products/rfid-nfc/mifare-hf/mifare-desfire)

## License

This project is licensed under the MIT License.
