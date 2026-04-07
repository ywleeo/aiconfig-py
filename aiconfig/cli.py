"""CLI entry point: aiconfig <command>."""

import time

import click
import httpx

from aiconfig import ConfigError, get_config
from aiconfig.config import encrypt_all, get_key, load, remove_key, set_key
from aiconfig.providers import MODEL_INDEX, PROVIDERS


@click.group()
def cli():
    """Global AI API key manager. Configure once, use everywhere."""


@cli.command("set")
@click.argument("provider")
@click.argument("api_key")
def set_cmd(provider: str, api_key: str):
    """Set API key for a provider (auto-encrypted)."""
    if provider not in PROVIDERS:
        click.echo(f"Unknown provider: {provider}")
        click.echo(f"Available: {', '.join(sorted(PROVIDERS.keys()))}")
        return
    set_key(provider, api_key)
    click.echo(f"✓ {provider} key saved (encrypted).")


@cli.command("list")
def list_cmd():
    """List configured providers and their models."""
    data = load()
    if not data:
        click.echo("No keys configured. Run: aiconfig set <provider> <key>")
        return
    for provider, key in sorted(data.items()):
        models = PROVIDERS.get(provider, {}).get("models", {})
        click.echo(f"\n{provider} (key: ...{key[-4:]})")
        for m in models:
            click.echo(f"  - {m}")


@cli.command()
def encrypt():
    """Encrypt any plaintext keys in keys.yaml."""
    count = encrypt_all()
    if count:
        click.echo(f"✓ {count} key(s) encrypted.")
    else:
        click.echo("All keys are already encrypted.")


@cli.command()
@click.argument("provider")
def remove(provider: str):
    """Remove a provider's API key."""
    if remove_key(provider):
        click.echo(f"✓ {provider} key removed.")
    else:
        click.echo(f"No key found for {provider}.")


@cli.command()
@click.argument("model")
def check(model: str):
    """Check if a model is ready (key configured)."""
    info = MODEL_INDEX.get(model)
    if not info:
        click.echo(f"Unknown model: {model}")
        return
    provider = info["provider"]
    if get_key(provider):
        click.echo(f"✓ {model} ready (provider: {provider})")
    else:
        click.echo(f"✗ {model} needs key. Run: aiconfig set {provider} <key>")


@cli.command()
@click.argument("model")
def test(model: str):
    """Test model connectivity and measure response time."""
    try:
        conf = get_config(model)
    except ConfigError as e:
        click.echo(f"✗ {e}")
        return

    click.echo(f"Testing {model} ({conf['provider']})...")
    click.echo(f"  base_url: {conf['base_url']}")

    provider_base = PROVIDERS[conf["provider"]]["base_url"]
    is_text_model = conf["base_url"] == provider_base

    start = time.time()
    if is_text_model:
        _test_text_model(conf, start)
    else:
        _test_connectivity(conf, start)


def _test_text_model(conf: dict, start: float) -> None:
    from openai import OpenAI

    try:
        client = OpenAI(base_url=conf["base_url"], api_key=conf["api_key"])
        client.chat.completions.create(
            model=conf["model"],
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=1,
        )
        click.echo(f"✓ Connected in {time.time() - start:.2f}s")
    except Exception as e:
        click.echo(f"✗ Failed after {time.time() - start:.2f}s: {e}")


def _test_connectivity(conf: dict, start: float) -> None:
    try:
        httpx.head(conf["base_url"], timeout=10)
        click.echo(f"✓ Reachable in {time.time() - start:.2f}s (non-text model, connectivity only)")
    except Exception as e:
        click.echo(f"✗ Unreachable after {time.time() - start:.2f}s: {e}")


@cli.command()
def models():
    """List all supported models."""
    for provider, pinfo in sorted(PROVIDERS.items()):
        key = get_key(provider)
        status = "✓" if key else "✗"
        click.echo(f"\n{status} {provider}")
        for m in pinfo["models"]:
            click.echo(f"    {m}")
