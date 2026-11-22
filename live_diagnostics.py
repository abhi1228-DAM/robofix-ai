import subprocess

CONTAINER = "autofleet-desktop"

CHECKS = {
    "ROS 2 Nodes": "ros2 node list --no-daemon",
    "ROS 2 Topics": "ros2 topic list",
    "ROS 2 Services": "ros2 service list",
}

def collect_diagnostics():
    results = {}

    for title, command in CHECKS.items():
        try:
            process = subprocess.run(
                [
                    "docker", "exec", "--user", "ubuntu", CONTAINER,
                    "bash", "-lc",
                    "source /opt/ros/humble/setup.bash && "
                    + command,
                ],
                capture_output=True,
                text=True,
                timeout=25,
                check=False,
            )

            output = (
                process.stdout.strip()
                or process.stderr.strip()
                or "(No results)"
            )

            if process.returncode != 0:
                output = (
                    f"Command failed with exit code "
                    f"{process.returncode}:\n{output}"
                )

            results[title] = output[:6000]

        except subprocess.TimeoutExpired:
            results[title] = "Diagnostic timed out."

        except FileNotFoundError:
            results[title] = (
                "Docker CLI not found on this computer."
            )

    report = "# Live ROS 2 Diagnostics\n\n"

    for title, output in results.items():
        report += f"## {title}\n\n"
        report += f"```\n{output}\n```\n\n"

    return results, report
