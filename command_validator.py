import re
import shlex

ALLOWED_COMMANDS = {
    ("ros2", "node", "list"),
    ("ros2", "node", "info"),
    ("ros2", "topic", "list"),
    ("ros2", "topic", "info"),
    ("ros2", "topic", "echo"),
    ("ros2", "topic", "hz"),
    ("ros2", "service", "list"),
    ("ros2", "service", "type"),
    ("ros2", "pkg", "list"),
    ("ros2", "interface", "show"),
    ("ros2", "param", "list"),
    ("ros2", "param", "get"),
}

def validate_command(command):
    command = command.strip()

    try:
        parts = shlex.split(command)
    except ValueError:
        return False, "Invalid command syntax"

    if len(parts) < 3:
        return False, "Incomplete ROS 2 command"

    if any(token in parts for token in [";", "&&", "||", "|", ">", "<"]):
        return False, "Shell operators require manual review"

    if re.search(r'[`$]', command):
        return False, "Shell expansion requires manual review"

    key = tuple(parts[:3])

    if key in ALLOWED_COMMANDS:
        return True, "Recognized read-only ROS 2 diagnostic command"

    return False, "Unverified or unsupported command"

def extract_commands(text):
    commands = []

    for line in text.splitlines():
        line = line.strip().lstrip("-* ")

        if line.startswith("ros2 "):
            commands.append(line)

    return commands
