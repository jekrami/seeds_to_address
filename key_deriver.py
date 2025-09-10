# key_deriver.py
#
# A comprehensive Python script for generating and deriving cryptographic keys and addresses
# for various cryptocurrencies based on BIP39 mnemonic phrases.
#
# Features:
# - Generates new BIP39 mnemonics or loads them from a 'seeds.csv' file.
# - Supports user-specified number of mnemonics, entropy strength, and address count.
# - Accommodates an optional BIP39 passphrase for enhanced security.
# - Derives keys for a wide range of cryptocurrencies and derivation paths.
# - Outputs detailed key information into separate CSV files for each coin.
# - Operates entirely offline, ensuring private keys are not exposed to the internet.
# - Designed with modularity to easily support additional cryptocurrencies.

import argparse
import csv
import os
import sys
import time
from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator, Bip39Languages
)
from config import COIN_CONFIG
from bip_utils.bip.bip44_base import Bip44Changes
from bip_utils.cardano.bip32 import CardanoIcarusBip32

def print_security_warning():
    """
    Prints a security warning to the user.
    """
    print("=======================================================================")
    print("SECURITY WARNING:")
    print("=======================================================================")
    print("This script generates and displays sensitive cryptographic information,")
    print("including private keys. Please use this script responsibly.")
    print("\n- DO NOT use these keys for storing real funds on a live wallet.")
    print("- This tool is intended for educational, testing, or recovery purposes ONLY.")
    print("- Ensure this script is run in a secure, offline environment.")
    print("- You are responsible for the secure handling of the generated files.")
    print("=======================================================================\n")

def get_bip39_language_from_name(lang_name):
    """
    Retrieves the Bip39Languages enum member from its string name.
    """
    try:
        return Bip39Languages[lang_name.upper()]
    except KeyError:
        print(f"Error: Language '{lang_name}' is not a valid BIP39 language.")
        # Listing all available languages for user convenience
        available_languages = [lang.name for lang in Bip39Languages]
        print("Available languages are:", ", ".join(available_languages))
        sys.exit(1)

def get_mnemonics(args):
    """
    Loads mnemonics from 'seeds.csv' if it exists, otherwise generates new ones.
    """
    if os.path.exists('seeds.csv'):
        print("Found 'seeds.csv'. Loading mnemonics from file...")
        with open('seeds.csv', 'r') as f:
            # Reads each line, strips whitespace/newlines, and filters out empty lines
            return [line.strip() for line in f if line.strip()]
    else:
        print(f"Generating {args.num_mnemonics} new mnemonic(s)...")
        # Determine the language for mnemonic generation
        language_enum = get_bip39_language_from_name(args.lang)
        mnemo = Mnemonic(language=language_enum.name.lower())
        # Strength is determined by the entropy bits
        strength = {128: 12, 160: 15, 192: 18, 224: 21, 256: 24}[args.strength]
        return [mnemo.generate(strength=args.strength) for _ in range(args.num_mnemonics)]


def derive_and_collect_keys(mnemonics, passphrase, num_addresses):
    """
    Derives keys for all configured coins from the given mnemonics and collects the data.
    """
    results = {coin: [] for coin in COIN_CONFIG}

    for i, mnemonic in enumerate(mnemonics):
        print(f"\rProcessing mnemonic {i+1}/{len(mnemonics)}...", end="")

        # Generate the seed from the mnemonic and optional passphrase
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)

        for coin_ticker, coin_info in COIN_CONFIG.items():
            for path_info in coin_info['paths']:
                bip_class = path_info['bip_class']
                coin_type = path_info['coin_type']

                # Instantiate the BIP class from the seed
                if coin_type is not None:
                    bip_obj_mst = bip_class.FromSeed(seed_bytes, coin_type)
                else:
                    bip_obj_mst = bip_class.FromSeed(seed_bytes)

                for i in range(num_addresses):
                    # Format the derivation path with the current index
                    deriv_path = path_info['path'].format(i)

                    # Derive the child key using the correct method for the class
                    if bip_class is CardanoIcarusBip32:
                        # Cardano uses DerivePath directly
                        bip_obj_child = bip_obj_mst.DerivePath(deriv_path)
                    else:
                        # Standard BIP44/49/84/86 derivation
                        # All paths in the config use account 0 and external change (0)
                        bip_obj_child = bip_obj_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)

                    # Collect the key data
                    data = {
                        "mnemonic": mnemonic,
                        "passphrase": passphrase or "",
                        "derivation_path": deriv_path,
                        "index": i,
                        "private_key": bip_obj_child.PrivateKey().Raw().ToHex(),
                        "public_key": "N/A",
                        "address": "N/A",
                        "chain_code": "N/A",
                        "fingerprint": "N/A",
                        "parent_public_key": "N/A"
                    }
                    results[coin_ticker].append(data)

    print("\nKey derivation complete.")
    return results

def write_results_to_csv(results):
    """
    Writes the collected key data to separate CSV files for each coin.
    """
    timestamp = int(time.time())
    for coin_ticker, data in results.items():
        if not data:
            continue

        filename = f"{coin_ticker}_{timestamp}.csv"
        print(f"Writing results to {filename}...")

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def main():
    """
    Main function to orchestrate the key derivation process.
    """
    print_security_warning()

    parser = argparse.ArgumentParser(description="BIP39 Mnemonic and Key Deriver")
    parser.add_argument("--num-mnemonics", type=int, default=3, help="Number of mnemonics to generate (default: 3).")
    parser.add_argument("--strength", type=int, choices=[128, 160, 192, 224, 256], default=128, help="Entropy strength in bits for new mnemonics (default: 128).")
    parser.add_argument("--num-addresses", type=int, default=1, help="Number of consecutive addresses to derive per path (default: 1).")
    parser.add_argument("--passphrase", type=str, default="", help="Optional BIP39 passphrase.")
    parser.add_argument("--lang", type=str, default="ENGLISH", help="Language for the mnemonic wordlist (e.g., ENGLISH, SPANISH, FRENCH). Default is ENGLISH.")

    args = parser.parse_args()

    mnemonics = get_mnemonics(args)
    if not mnemonics:
        print("No mnemonics to process. Exiting.")
        return

    results = derive_and_collect_keys(mnemonics, args.passphrase, args.num_addresses)
    write_results_to_csv(results)

    print("\nProcess finished successfully.")
    print("Generated CSV files are in the current directory.")

if __name__ == "__main__":
    main()
