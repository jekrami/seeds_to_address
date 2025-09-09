# BIP39 Wallet Tool

A command-line tool for generating and managing BIP39 wallets, including mnemonic generation, validation, and address derivation for Bitcoin and Ethereum.

## Features

- **Mnemonic Generation**: Create secure BIP39 mnemonics with 128, 160, 192, 224, or 256 bits of entropy (12, 15, 18, 21, or 24 words).
- **Mnemonic Validation**: Check if an existing mnemonic phrase is valid.
- **Seed Derivation**: Generate a cryptographic seed from a mnemonic.
- **Address Generation**: Derive Bitcoin (P2PKH) and Ethereum addresses from a mnemonic.
- **CSV Output**: Export generated wallet data in CSV format.
- **File Input**: Read a list of mnemonics from a text file to derive wallets in bulk.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

The tool is operated via the command line with three main sub-commands: `generate`, `validate`, and `from-file`.

### 1. Generate Wallets

Create one or more new wallets.

**Basic Usage:**
```bash
python bip39_wallet.py generate
```

**Options:**
- `-n`, `--number <N>`: Specify the number of wallets to generate (default: 1).
- `--strength <BITS>`: Set the entropy strength. Options: 128 (default), 160, 192, 224, 256.
- `--csv`: Output the results in CSV format.

**Examples:**

- **Generate a single wallet with default strength (128-bit):**
  ```bash
  python bip39_wallet.py generate
  ```
  *Example Output:*
  ```
  Mnemonic: word1 word2 ... word12
  Seed: <seed_hex_string>
  Bitcoin Address (P2PKH): <btc_address>
  Ethereum Address: <eth_address>
  --------------------
  ```

- **Generate 3 wallets with 256-bit strength:**
  ```bash
  python bip39_wallet.py generate --number 3 --strength 256
  ```

- **Generate 5 wallets and output to CSV:**
  ```bash
  python bip39_wallet.py generate --number 5 --csv > wallets.csv
  ```
  *wallets.csv will contain:*
  ```csv
  mnemonic,seed,btc_address,eth_address
  "...", "...", "...", "..."
  ```

### 2. Validate a Mnemonic

Check if a mnemonic phrase is valid according to the BIP39 standard.

**Usage:**
```bash
python bip39_wallet.py validate "<your-mnemonic-phrase>"
```

**Examples:**

- **Validate a valid mnemonic:**
  ```bash
  python bip39_wallet.py validate "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
  ```
  *Output:* `Mnemonic is valid.`

- **Validate an invalid mnemonic:**
  ```bash
  python bip39_wallet.py validate "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
  ```
  *Output:* `Mnemonic is invalid.`

### 3. Derive Wallets from a File

Read a text file containing one mnemonic per line and derive wallets for each.

**Usage:**
```bash
python bip39_wallet.py from-file <path-to-your-file.txt>
```

**Options:**
- `--csv`: Output the results in CSV format.

**Example:**

1.  Create a file named `seeds.txt` with the following content:
    ```
    legal winner thank year wave sausage worth useful legal winner thank yellow
    abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
    ```

2.  Run the command:
    ```bash
    python bip39_wallet.py from-file seeds.txt
    ```

3.  To output to CSV:
    ```bash
    python bip39_wallet.py from-file seeds.txt --csv > derived_wallets.csv
    ```

## Testing

To ensure all functionality is working correctly, run the test suite:
```bash
python test_wallet.py
```
