from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str) -> str:
    """Load a prompt from a markdown file."""
    return (PROMPTS_DIR / f"{name}.md").read_text()
