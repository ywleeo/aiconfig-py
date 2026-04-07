"""aiconfig - Global AI API key manager. Configure once, use everywhere."""

__all__ = ["get_config", "ConfigError"]


class ConfigError(Exception):
    """Raised when model is unknown or key is not configured."""


def get_config(model: str) -> dict:
    """Get config for a model by name.

    Returns: {"provider": str, "base_url": str, "api_key": str, "model": str}
    Raises: ConfigError
    """
    from aiconfig.config import get_key
    from aiconfig.providers import MODEL_INDEX

    info = MODEL_INDEX.get(model)
    if not info:
        raise ConfigError(
            f"Unknown model: {model}. "
            f"Run 'aiconfig models' to see available models."
        )

    provider = info["provider"]
    api_key = get_key(provider)
    if not api_key:
        raise ConfigError(
            f"No API key for provider '{provider}'. "
            f"Run: aiconfig set {provider} <your-key>"
        )

    return {
        "provider": provider,
        "base_url": info["base_url"],
        "api_key": api_key,
        "model": model,
    }
