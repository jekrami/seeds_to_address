import unittest
from bip39_wallet import (
    generate_mnemonic,
    validate_mnemonic,
    derive_wallet_from_mnemonic
)

class TestBip39Wallet(unittest.TestCase):

    def test_generate_mnemonic(self):
        strengths = {
            128: 12,
            160: 15,
            192: 18,
            224: 21,
            256: 24
        }
        for strength, words in strengths.items():
            mnemonic = generate_mnemonic(strength)
            self.assertEqual(len(str(mnemonic).split()), words)
            self.assertTrue(validate_mnemonic(str(mnemonic)))

    def test_validate_mnemonic(self):
        # Known valid mnemonic
        valid_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        self.assertTrue(validate_mnemonic(valid_mnemonic))

        # Known invalid mnemonic (bad checksum)
        invalid_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
        self.assertFalse(validate_mnemonic(invalid_mnemonic))

        # Invalid word count
        invalid_word_count = "abandon abandon"
        self.assertFalse(validate_mnemonic(invalid_word_count))

        # Invalid word
        invalid_word = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon xyz"
        self.assertFalse(validate_mnemonic(invalid_word))

    def test_derive_wallet_from_mnemonic(self):
        # Using a known test vector
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        expected_wallet = {
            "mnemonic": mnemonic,
            "seed": "5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4",
            "btc_address": "1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA",
            "eth_address": "0x9858EfFD232B4033E47d90003D41EC34EcaEda94"
        }

        wallet = derive_wallet_from_mnemonic(mnemonic)
        self.assertEqual(wallet["seed"], expected_wallet["seed"])
        self.assertEqual(wallet["btc_address"], expected_wallet["btc_address"])
        self.assertEqual(wallet["eth_address"], expected_wallet["eth_address"])

    def test_derive_from_invalid_mnemonic(self):
        invalid_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
        with self.assertRaises(ValueError):
            derive_wallet_from_mnemonic(invalid_mnemonic)

if __name__ == '__main__':
    unittest.main()
