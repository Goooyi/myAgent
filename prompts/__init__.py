from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str) -> str:
    """Load a prompt from a markdown file.

    Args:
        name: Prompt name (without .md extension)

    Returns:
        Prompt content as string
    """
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text()


def list_prompts() -> list[str]:
    """List all available prompts."""
    return [p.stem for p in PROMPTS_DIR.glob("*.md")]
