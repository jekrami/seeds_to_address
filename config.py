# config.py
#
# This file contains the configuration for the cryptocurrencies to be used in the key deriver script.
# Each coin is represented as a dictionary with its name, and a list of derivation paths.
# This modular approach allows for easy addition or modification of coins and their paths.

from bip_utils import (
    Bip44Coins, Bip49Coins, Bip84Coins, Bip86Coins
)
from bip_utils.bip.bip44 import Bip44
from bip_utils.bip.bip49 import Bip49
from bip_utils.bip.bip84 import Bip84
from bip_utils.bip.bip86 import Bip86
from bip_utils.cardano.bip32 import CardanoIcarusBip32

# A dictionary defining the configuration for each supported cryptocurrency.
# Each key is a coin ticker symbol, and the value is a dictionary containing:
# 'name': The full name of the cryptocurrency.
# 'paths': A list of dictionaries, where each dictionary represents a derivation path and contains:
#   'name': A descriptive name for the path (e.g., "Legacy", "SegWit").
#   'path': The BIP derivation path string.
#   'bip_class': The main BIP class from bip_utils (e.g., Bip44, Bip49).
#   'coin_type': The specific coin enum from bip_utils (e.g., Bip44Coins.BITCOIN).
COIN_CONFIG = {
    "BTC": {
        "name": "Bitcoin",
        "paths": [
            {"name": "Legacy", "path": "m/44'/0'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.BITCOIN},
            {"name": "Nested SegWit", "path": "m/49'/0'/0'/0/{}", "bip_class": Bip49, "coin_type": Bip49Coins.BITCOIN},
            {"name": "Native SegWit", "path": "m/84'/0'/0'/0/{}", "bip_class": Bip84, "coin_type": Bip84Coins.BITCOIN},
            {"name": "Taproot", "path": "m/86'/0'/0'/0/{}", "bip_class": Bip86, "coin_type": Bip86Coins.BITCOIN},
        ]
    },
    "ETH": {
        "name": "Ethereum",
        "paths": [
            {"name": "EVM", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.ETHEREUM},
        ]
    },
    "BSC": {
        "name": "Binance Smart Chain",
        "paths": [
            {"name": "EVM", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.BINANCE_SMART_CHAIN},
        ]
    },
    "POLYGON": {
        "name": "Polygon",
        "paths": [
            {"name": "EVM", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.POLYGON},
        ]
    },
    "AVAX": {
        "name": "Avalanche",
        "paths": [
            {"name": "EVM", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.AVAX_C_CHAIN},
        ]
    },
    "ARBITRUM": {
        "name": "Arbitrum",
        "paths": [
            {"name": "EVM", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.ARBITRUM},
        ]
    },
    "OPTIMISM": {
        "name": "Optimism",
        "paths": [
            {"name": "EVM", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.OPTIMISM},
        ]
    },
    "ADA": {
        "name": "Cardano",
        "paths": [
            {"name": "Icarus", "path": "m/1852'/1815'/0'/0/{}", "bip_class": CardanoIcarusBip32, "coin_type": None},
        ]
    },
    "XRP": {
        "name": "Ripple",
        "paths": [
            {"name": "Default", "path": "m/44'/144'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.RIPPLE},
        ]
    },
    "LTC": {
        "name": "Litecoin",
        "paths": [
            {"name": "Legacy", "path": "m/44'/2'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.LITECOIN},
            {"name": "Nested SegWit", "path": "m/49'/2'/0'/0/{}", "bip_class": Bip49, "coin_type": Bip49Coins.LITECOIN},
            {"name": "Native SegWit", "path": "m/84'/2'/0'/0/{}", "bip_class": Bip84, "coin_type": Bip84Coins.LITECOIN},
        ]
    },
    "DOGE": {
        "name": "Dogecoin",
        "paths": [
            {"name": "Default", "path": "m/44'/3'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.DOGECOIN},
        ]
    },
    "BCH": {
        "name": "Bitcoin Cash",
        "paths": [
            {"name": "Default", "path": "m/44'/145'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.BITCOIN_CASH},
        ]
    },
    "DOT": {
        "name": "Polkadot",
        "paths": [
            {"name": "Default", "path": "m/44'/354'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.POLKADOT_ED25519_SLIP},
        ]
    },
    "USDT": {
        "name": "Tether",
        "paths": [
            {"name": "ERC20 (ETH)", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.ETHEREUM},
            {"name": "BEP20 (BSC)", "path": "m/44'/60'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.BINANCE_SMART_CHAIN},
            {"name": "Omni (BTC Legacy)", "path": "m/44'/0'/0'/0/{}", "bip_class": Bip44, "coin_type": Bip44Coins.BITCOIN},
        ]
    }
}
