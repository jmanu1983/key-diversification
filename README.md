# Outil de diversification de clés

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![PyCryptodome](https://img.shields.io/badge/Crypto-AES%2FCMAC-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

Outil de **diversification de clés AES/CMAC** avec interface graphique tkinter, implémentant la spécification NXP AN10922 pour la diversification des clés MIFARE DESFire. Utilisé dans les systèmes de contrôle d'accès pour dériver des clés carte uniques à partir d'une clé maître.

## Fonctionnement

L'outil calcule une clé AES-128 diversifiée en utilisant :

1. **Entrée** : UID + Application ID + Données fixes + Clé maître (EMK)
2. **Traitement** : Ajout de la constante `0x01`, application du padding CMAC, calcul AES-CMAC
3. **Sortie** : Clé diversifiée de 128 bits, unique à la carte

```
Clé diversifiée = AES-CMAC(EMK, 0x01 || UID || APPID_DYNAMIC || FIX)
```

## Stack technique

| Composant | Technologie |
|-----------|------------|
| Langage | Python 3.9+ |
| Cryptographie | PyCryptodome (AES, CMAC) |
| Interface | tkinter |

## Installation

```bash
git clone https://github.com/jmanu1983/key-diversification.git
cd key-diversification

pip install -r requirements.txt
```

## Utilisation

```bash
python Diversification_v4.py
```

L'interface s'ouvre avec les champs suivants :

| Champ | Description | Exemple |
|-------|------------|---------|
| UID | Identifiant unique de la carte (hex) | `04A23BC1D52E80` |
| APPID_DYNAMIC | Identifiant d'application (hex) | `F54100` |
| FIX | Données fixes de diversification (hex) | `4E585020416275` |
| EMK | Clé maître de chiffrement (hex) | `00112233445566778899AABBCCDDEEFF` |

Cliquer sur **Diversifier** pour calculer la clé diversifiée.

## Structure du projet

```
key-diversification/
├── Diversification_v4.py   # Application principale (dernière version)
├── requirements.txt        # Dépendances Python
└── README.md
```

## Références

- [NXP AN10922 — Diversification de clés AES](https://www.nxp.com/docs/en/application-note/AN10922.pdf)
- [Documentation MIFARE DESFire EV1/EV2](https://www.nxp.com/products/rfid-nfc/mifare-hf/mifare-desfire)

## Licence

Ce projet est sous licence MIT.
