import subprocess
import time

CONTAINER = "autofleet-desktop"

CHECKS = {
    "ROS 2 Nodes": "ros2 node list --no-daemon",
    "ROS 2 Topics": "ros2 topic list",
    "ROS 2 Services": "ros2 service list",
}


def run_ros_command(command):
    return subprocess.run(
        [
            "docker", "exec", "--user", "ubuntu", CONTAINER,
            "bash", "-lc",
            "source /opt/ros/humble/setup.bash && " + command,
        ],
        capture_output=True,
        text=True,
        timeout=25,
        check=False,
    )


def collect_diagnostics():
    results = {}

    for title, command in CHECKS.items():
        try:
            attempts = 3 if title == "ROS 2 Nodes" else 1
            output = ""

            for attempt in range(attempts):
                process = run_ros_command(command)

                if process.returncode != 0:
                    output = (
                        f"Command failed with exit code "
                        f"{process.returncode}:\n"
                        f"{process.stderr.strip() or process.stdout.strip()}"
                    )
                    break

                output = process.stdout.strip()

                if output:
                    break

                if attempt < attempts - 1:
                    time.sleep(1)

            if process.returncode == 0 and not output:
                if title == "ROS 2 Nodes":
                    output = (
                        "Node discovery inconclusive after "
                        f"{attempts} attempts."
                    )
                else:
                    output = "(No results)"

            results[title] = output[:6000]

        except subprocess.TimeoutExpired:
            results[title] = "Diagnostic timed out."

        except FileNotFoundError:
            results[title] = "Docker CLI not found on this computer."

    report = "# Live ROS 2 Diagnostics\n\n"

    for title, output in results.items():
        report += f"## {title}\n\n"
        report += f"```\n{output}\n```\n\n"

    return results, report
