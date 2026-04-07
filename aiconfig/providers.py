"""Load provider registry from providers.yaml."""

from pathlib import Path

import yaml

_DIR = Path(__file__).parent
PROVIDERS_FILE = _DIR / "providers.yaml"


def load_providers() -> dict[str, dict]:
    return yaml.safe_load(PROVIDERS_FILE.read_text()) or {}


def build_model_index(providers: dict[str, dict]) -> dict[str, dict]:
    """Build model_name -> {provider, base_url} index."""
    index: dict[str, dict] = {}
    for provider, pinfo in providers.items():
        default_url = pinfo["base_url"]
        for model, minfo in pinfo.get("models", {}).items():
            index[model] = {
                "provider": provider,
                "base_url": minfo.get("base_url", default_url) if minfo else default_url,
            }
    return index


PROVIDERS = load_providers()
MODEL_INDEX = build_model_index(PROVIDERS)
