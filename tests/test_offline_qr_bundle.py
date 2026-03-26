import random
import secrets
import unittest

from tools.offline_qr_bundle import BundleError, pack_bytes, unpack_payloads


class OfflineQrBundleTests(unittest.TestCase):
    def test_roundtrip_single_chunk(self) -> None:
        raw = b"hello offline qr"
        payloads = pack_bytes(raw, max_qr_chars=900)
        out = unpack_payloads(payloads)
        self.assertEqual(out, raw)

    def test_roundtrip_multi_chunk_with_shuffle(self) -> None:
        raw = secrets.token_bytes(7000)
        payloads = pack_bytes(raw, max_qr_chars=420)
        self.assertGreater(len(payloads), 1)

        shuffled = payloads[:]
        random.shuffle(shuffled)
        out = unpack_payloads(shuffled)
        self.assertEqual(out, raw)

    def test_missing_chunk_should_fail(self) -> None:
        raw = secrets.token_bytes(6000)
        payloads = pack_bytes(raw, max_qr_chars=350)
        self.assertGreater(len(payloads), 1)

        bad = payloads[:-1]
        with self.assertRaises(BundleError):
            unpack_payloads(bad)

    def test_tamper_chunk_should_fail(self) -> None:
        raw = secrets.token_bytes(5000)
        payloads = pack_bytes(raw, max_qr_chars=380)
        self.assertGreater(len(payloads), 1)

        tampered = payloads[:]
        tampered[0] = tampered[0].replace('"d":"', '"d":"x', 1)

        with self.assertRaises(BundleError):
            unpack_payloads(tampered)


if __name__ == "__main__":
    unittest.main()
