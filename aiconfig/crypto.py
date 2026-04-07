"""Machine-fingerprint based encryption for API keys."""

import base64
import getpass
import hashlib
import uuid

from cryptography.fernet import Fernet

# Encrypted values are prefixed with this to distinguish from plaintext
ENC_PREFIX = "enc:"


def _get_machine_key() -> bytes:
    """Derive a Fernet key from machine fingerprint (MAC + username)."""
    mac = str(uuid.getnode())
    user = getpass.getuser()
    seed = f"aiconfig:{mac}:{user}".encode()
    # SHA-256 → 32 bytes → base64 → Fernet key
    digest = hashlib.sha256(seed).digest()
    return base64.urlsafe_b64encode(digest)


_fernet = Fernet(_get_machine_key())


def encrypt(plaintext: str) -> str:
    """Encrypt a string, return with enc: prefix."""
    token = _fernet.encrypt(plaintext.encode()).decode()
    return f"{ENC_PREFIX}{token}"


def decrypt(value: str) -> str:
    """Decrypt if enc: prefixed, otherwise return as-is (plaintext)."""
    if not value.startswith(ENC_PREFIX):
        return value
    token = value[len(ENC_PREFIX):]
    return _fernet.decrypt(token.encode()).decode()
