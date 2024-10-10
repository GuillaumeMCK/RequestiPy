import keyword
import re

from models.colors import colors


def python_highlight(textbox):
    """Applies basic Python syntax highlighting to the content of a CTkTextbox."""

    # Clear existing tags
    textbox.tag_remove("keyword", "1.0", "end")
    textbox.tag_remove("comment", "1.0", "end")
    textbox.tag_remove("string", "1.0", "end")
    textbox.tag_remove("int", "1.0", "end")
    textbox.tag_remove("float", "1.0", "end")

    # Define syntax highlighting colors
    textbox.tag_config("keyword", foreground=colors.blue)
    textbox.tag_config("comment", foreground=colors.lerp(colors.grey, colors.content2, 0.5))
    textbox.tag_config("string", foreground=colors.lerp(colors.green, colors.content2, 0.5))
    textbox.tag_config("int", foreground=colors.pink)
    textbox.tag_config("float", foreground=colors.purple)

    # Get the full text from the textbox
    content = textbox.get("1.0", "end")

    # Split the content into lines
    lines = content.split("\n")

    # Loop through each line
    for i, line in enumerate(lines):
        # Highlight keywords
        for word in keyword.kwlist:
            matches = re.finditer(rf"\b{word}\b", line)
            for match in matches:
                start_index = f"{i + 1}.{match.start()}"
                end_index = f"{i + 1}.{match.end()}"
                textbox.tag_add("keyword", start_index, end_index)

        # Highlight comments
        if "#" in line:
            comment_start = line.index("#")
            start_index = f"{i + 1}.{comment_start}"
            end_index = f"{i + 1}.end"
            textbox.tag_add("comment", start_index, end_index)

        # Highlight strings
        matches = re.finditer(r'(".*?"|\'.*?\')', line)
        for match in matches:
            start_index = f"{i + 1}.{match.start()}"
            end_index = f"{i + 1}.{match.end()}"
            textbox.tag_add("string", start_index, end_index)

        # Colors integers to pink and floats to purple
        matches = re.finditer(r'\b\d+\b', line)
        for match in matches:
            start_index = f"{i + 1}.{match.start()}"
            end_index = f"{i + 1}.{match.end()}"
            textbox.tag_add("int", start_index, end_index)

        matches = re.finditer(r'\b\d+\.\d+\b', line)
        for match in matches:
            start_index = f"{i + 1}.{match.start()}"
            end_index = f"{i + 1}.{match.end()}"
            textbox.tag_add("float", start_index, end_index)


def header_highlight(textbox):
    """Applies basic syntax highlighting to HTTP headers."""

    # Clear existing tags
    textbox.tag_remove("method", "1.0", "end")
    textbox.tag_remove("key", "1.0", "end")
    textbox.tag_remove("value", "1.0", "end")
    textbox.tag_remove("comment", "1.0", "end")
    textbox.tag_remove("variable", "1.0", "end")

    # Define syntax highlighting colors
    textbox.tag_config("method", foreground=colors.blue)
    textbox.tag_config("key", foreground=colors.magenta)
    textbox.tag_config("value", foreground=colors.orange)
    textbox.tag_config("comment", foreground=colors.green)
    textbox.tag_config("variable", foreground=colors.white)

    # Get the full text from the textbox
    content = textbox.get("1.0", "end")

    # Split the content into lines
    lines = content.split("\n")

    # Define HTTP methods
    methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"}

    lines = [line for line in lines if line.strip()]

    # Loop through each line
    for i, line in enumerate(lines):
        words = line.strip().split()
        if words and words[0] in methods:
            method = words[0]
            start_index = f"{i + 1}.0"
            end_index = f"{i + 1}.{len(method)}"
            textbox.tag_add("method", start_index, end_index)

        # Highlight header keys and values
        if ":" in line:
            key, value = line.split(":", 1)
            key_start = f"{i + 1}.0"
            key_end = f"{i + 1}.{len(key)}"
            value_start = f"{i + 1}.{len(key) + 1}"  # Start after the colon
            value_end = f"{i + 1}.end"

            # Apply tags
            textbox.tag_add("key", key_start, key_end)
            textbox.tag_add("value", value_start, value_end)

        # Highlight comments (lines starting with "#")
        if line.strip().startswith("#"):
            comment_start = f"{i + 1}.0"
            comment_end = f"{i + 1}.end"
            textbox.tag_add("comment", comment_start, comment_end)

    # Highlight variables in the header
    pattern = re.compile(r"\$\$(.*?)\$\$")
    for match in pattern.finditer(content):
        start_index = f"1.{match.start()}"
        end_index = f"1.{match.end()}"
        textbox.tag_add("variable", start_index, end_index)


def body_highlight(textbox):
    """Applies basic syntax highlighting to $$key$$ tags in the body."""
    # Clear existing tags
    textbox.tag_remove("key", "1.0", "end")

    # Configure the highlighting for key tags
    textbox.tag_config("key", foreground=colors.white)

    # Define the pattern for $$key$$ tags
    pattern = re.compile(r"\$\$(.*?)\$\$")

    # Get the full text from the textbox and strip whitespace
    content = textbox.get("1.0", "end").strip()
    if not content:
        return

    # Use regex to find all $$key$$ tags in the content
    for match in pattern.finditer(content):
        if match:
            start_index = f"1.{match.start()}"
            end_index = f"1.{match.end()}"
            textbox.tag_add("key", start_index, end_index)
        else:
            textbox.tag_add("default", "1.0", "1.end")
