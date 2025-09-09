import argparse
import csv
import sys
import os
from bip_utils import (
    Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum,
    Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicValidator
)
from bip_utils.utils.mnemonic.mnemonic_ex import MnemonicChecksumError

def generate_mnemonic(strength: int) -> str:
    """Generate a BIP39 mnemonic phrase."""
    words_num = Bip39WordsNum(strength // 32 * 3)
    return Bip39MnemonicGenerator().FromWordsNumber(words_num)

def validate_mnemonic(mnemonic: str) -> bool:
    """Validate a BIP39 mnemonic phrase."""
    try:
        Bip39MnemonicValidator().Validate(mnemonic)
        return True
    except (ValueError, MnemonicChecksumError):
        return False

def derive_wallet_from_mnemonic(mnemonic: str):
    """Derive BTC and ETH addresses from a mnemonic."""
    if not validate_mnemonic(mnemonic):
        raise ValueError("Invalid mnemonic phrase")

    # Generate seed from mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    # Derive Bitcoin address (P2PKH)
    bip44_btc_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip44_btc_acc = bip44_btc_mst.Purpose().Coin().Account(0)
    bip44_btc_addr = bip44_btc_acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    btc_address = bip44_btc_addr.PublicKey().ToAddress()

    # Derive Ethereum address
    bip44_eth_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    bip44_eth_acc = bip44_eth_mst.Purpose().Coin().Account(0)
    bip44_eth_addr = bip44_eth_acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    eth_address = bip44_eth_addr.PublicKey().ToAddress()

    return {
        "mnemonic": mnemonic,
        "seed": seed_bytes.hex(),
        "btc_address": btc_address,
        "eth_address": eth_address,
    }

def print_csv(wallets):
    """Print wallets in CSV format."""
    if not wallets:
        return
    writer = csv.DictWriter(sys.stdout, fieldnames=wallets[0].keys())
    writer.writeheader()
    writer.writerows(wallets)

def main():
    parser = argparse.ArgumentParser(description="A complete BIP39 wallet tool.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for generating mnemonics
    gen_parser = subparsers.add_parser("generate", help="Generate new mnemonics and wallets.")
    gen_parser.add_argument("--strength", type=int, choices=[128, 160, 192, 224, 256], default=128, help="Entropy strength in bits.")
    gen_parser.add_argument("-n", "--number", type=int, default=1, help="Number of wallets to generate.")
    gen_parser.add_argument("--csv", action="store_true", help="Output in CSV format.")

    # Sub-parser for validating mnemonics
    val_parser = subparsers.add_parser("validate", help="Validate a mnemonic phrase.")
    val_parser.add_argument("mnemonic", type=str, help="The mnemonic phrase to validate.")

    # Sub-parser for deriving from a file
    file_parser = subparsers.add_parser("from-file", help="Derive wallets from a file of mnemonics.")
    file_parser.add_argument("input_file", type=str, help="Path to the file containing mnemonics (one per line).")
    file_parser.add_argument("--csv", action="store_true", help="Output in CSV format.")

    args = parser.parse_args()

    if args.command == "generate":
        wallets = []
        for _ in range(args.number):
            mnemonic = generate_mnemonic(args.strength)
            wallet = derive_wallet_from_mnemonic(mnemonic)
            wallets.append(wallet)

        if args.csv:
            print_csv(wallets)
        else:
            for wallet in wallets:
                print(f"Mnemonic: {wallet['mnemonic']}")
                print(f"Seed: {wallet['seed']}")
                print(f"Bitcoin Address (P2PKH): {wallet['btc_address']}")
                print(f"Ethereum Address: {wallet['eth_address']}")
                print("-" * 20)

    elif args.command == "validate":
        if validate_mnemonic(args.mnemonic):
            print("Mnemonic is valid.")
        else:
            print("Mnemonic is invalid.")

    elif args.command == "from-file":
        if not os.path.exists(args.input_file):
            print(f"Error: File not found at '{args.input_file}'", file=sys.stderr)
            sys.exit(1)

        wallets = []
        with open(args.input_file, 'r') as f:
            for line in f:
                mnemonic = line.strip()
                if mnemonic:
                    try:
                        wallet = derive_wallet_from_mnemonic(mnemonic)
                        wallets.append(wallet)
                    except ValueError as e:
                        print(f"Skipping invalid mnemonic: '{mnemonic}'", file=sys.stderr)

        if args.csv:
            print_csv(wallets)
        else:
            for wallet in wallets:
                print(f"Mnemonic: {wallet['mnemonic']}")
                print(f"Seed: {wallet['seed']}")
                print(f"Bitcoin Address (P2PKH): {wallet['btc_address']}")
                print(f"Ethereum Address: {wallet['eth_address']}")
                print("-" * 20)

if __name__ == "__main__":
    main()
