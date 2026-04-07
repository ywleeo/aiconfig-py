"""Read/write keys.yaml with auto encryption."""

import os
from pathlib import Path

import yaml

from aiconfig.crypto import ENC_PREFIX, decrypt, encrypt

KEYS_FILE = Path(__file__).parent / "keys.yaml"


def _read_raw() -> dict[str, str | None]:
    if not KEYS_FILE.exists():
        return {}
    return yaml.safe_load(KEYS_FILE.read_text()) or {}


def _write_raw(data: dict) -> None:
    KEYS_FILE.write_text(yaml.dump(data, default_flow_style=False))
    os.chmod(KEYS_FILE, 0o600)


def load() -> dict[str, str]:
    """Load all keys, auto-decrypt. Returns {provider: plaintext_key}."""
    return {
        k: decrypt(v)
        for k, v in _read_raw().items()
        if v and isinstance(v, str)
    }


def get_key(provider: str) -> str | None:
    """Get a single decrypted key."""
    return load().get(provider)


def set_key(provider: str, api_key: str) -> None:
    """Set key (auto-encrypted)."""
    data = _read_raw()
    data[provider] = encrypt(api_key)
    _write_raw(data)


def remove_key(provider: str) -> bool:
    """Remove a key. Returns True if removed."""
    data = _read_raw()
    if data.get(provider):
        data[provider] = None
        _write_raw(data)
        return True
    return False


def encrypt_all() -> int:
    """Encrypt any plaintext keys. Returns count of newly encrypted."""
    data = _read_raw()
    count = 0
    for k, v in data.items():
        if v and isinstance(v, str) and not v.startswith(ENC_PREFIX):
            data[k] = encrypt(v)
            count += 1
    if count:
        _write_raw(data)
    return count
