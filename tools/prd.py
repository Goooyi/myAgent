"""PRD (Product Requirements Document) tools for PM agent.

PRDs are stored as Markdown files for better human readability.
"""

import re

from langchain_core.tools import tool


@tool(parse_docstring=True)
def parse_prd_to_mermaid(prd_markdown: str) -> str:
    """Convert PRD Markdown to Mermaid architecture diagram.

    Parses a PRD document in Markdown format and generates a Mermaid flowchart
    showing the system architecture and component relationships.

    Args:
        prd_markdown: PRD content in Markdown format

    Returns:
        Mermaid diagram code representing the architecture
    """
    lines = ["flowchart TD"]
    
    # Extract components from ## Components section
    components_match = re.search(
        r"##\s*Components?\s*\n(.*?)(?=\n##|\Z)", 
        prd_markdown, 
        re.DOTALL | re.IGNORECASE
    )
    
    if components_match:
        content = components_match.group(1)
        # Parse list items like "- **ComponentName**: description"
        for match in re.finditer(r"-\s*\*\*([^*]+)\*\*", content):
            name = match.group(1).strip()
            node_id = re.sub(r"[^a-zA-Z0-9]", "", name)
            lines.append(f"    {node_id}[{name}]")
    
    # Extract features from ## Features section
    features_match = re.search(
        r"##\s*Features?\s*\n(.*?)(?=\n##|\Z)", 
        prd_markdown, 
        re.DOTALL | re.IGNORECASE
    )
    
    if features_match:
        content = features_match.group(1)
        for match in re.finditer(r"-\s*\*\*([^*]+)\*\*", content):
            name = match.group(1).strip()
            node_id = re.sub(r"[^a-zA-Z0-9]", "", name)
            lines.append(f"    {node_id}[{name}]")
    
    # Extract dependencies from "depends on" or "->" patterns
    for match in re.finditer(r"(\w+)\s*(?:depends on|->|→)\s*(\w+)", prd_markdown, re.IGNORECASE):
        source, target = match.groups()
        source_id = re.sub(r"[^a-zA-Z0-9]", "", source)
        target_id = re.sub(r"[^a-zA-Z0-9]", "", target)
        lines.append(f"    {target_id} --> {source_id}")
    
    if len(lines) == 1:
        return "No components or features found. Ensure PRD has ## Components or ## Features sections with **bold** items."
    
    return "\n".join(lines)


@tool(parse_docstring=True)
def parse_mermaid_to_prd(mermaid: str) -> str:
    """Convert Mermaid architecture diagram to PRD Markdown.

    Parses a Mermaid flowchart and generates a structured PRD document
    in Markdown format.

    Args:
        mermaid: Mermaid diagram code

    Returns:
        PRD content in Markdown format
    """
    node_pattern = re.compile(r"(\w+)\[([^\]]+)\]")
    edge_pattern = re.compile(r"(\w+)\s*-->\s*(\w+)")

    node_names = {}
    for match in node_pattern.finditer(mermaid):
        node_id, name = match.groups()
        node_names[node_id] = name

    dependencies = {}
    for match in edge_pattern.finditer(mermaid):
        source, target = match.groups()
        if target not in dependencies:
            dependencies[target] = []
        if source in node_names:
            dependencies[target].append(node_names[source])

    # Build Markdown PRD
    lines = [
        "# Product Requirements Document",
        "",
        "## Overview",
        "",
        "*Add product description here*",
        "",
        "## Components",
        "",
    ]

    for node_id, name in node_names.items():
        deps = dependencies.get(node_id, [])
        if deps:
            lines.append(f"- **{name}**: Depends on {', '.join(deps)}")
        else:
            lines.append(f"- **{name}**")

    lines.extend([
        "",
        "## Features",
        "",
        "*Add features here*",
        "",
        "## User Stories",
        "",
        "*Add user stories here*",
    ])

    return "\n".join(lines)


@tool(parse_docstring=True)
def validate_prd(prd_markdown: str) -> dict:
    """Validate PRD completeness and structure.

    Checks a PRD Markdown document for required sections and content.

    Args:
        prd_markdown: PRD content in Markdown format

    Returns:
        Validation result with is_valid flag, errors list, and warnings list
    """
    errors = []
    warnings = []

    # Check for title (# heading)
    if not re.search(r"^#\s+.+", prd_markdown, re.MULTILINE):
        errors.append("Missing document title (# heading)")

    # Required sections
    required_sections = ["overview", "features"]
    for section in required_sections:
        if not re.search(rf"##\s*{section}", prd_markdown, re.IGNORECASE):
            errors.append(f"Missing required section: ## {section.title()}")

    # Check for features content
    features_match = re.search(
        r"##\s*Features?\s*\n(.*?)(?=\n##|\Z)", 
        prd_markdown, 
        re.DOTALL | re.IGNORECASE
    )
    if features_match:
        content = features_match.group(1).strip()
        if not content or content.startswith("*"):
            warnings.append("Features section appears empty or contains only placeholder text")
        elif not re.search(r"-\s+", content):
            warnings.append("Features section should use list format (- item)")

    # Recommended sections
    recommended_sections = ["user stories", "components", "acceptance criteria", "timeline"]
    for section in recommended_sections:
        if not re.search(rf"##\s*{section}", prd_markdown, re.IGNORECASE):
            warnings.append(f"Recommended section missing: ## {section.title()}")

    # Check for Mermaid diagram
    if not re.search(r"```mermaid", prd_markdown):
        warnings.append("Consider adding a Mermaid architecture diagram")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }
