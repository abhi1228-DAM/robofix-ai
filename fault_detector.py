def detect_faults(results, expected_nodes=None, expected_topics=None):
    faults = []

    def entries(output):
        return {
            line.strip()
            for line in output.splitlines()
            if line.strip().startswith("/")
        }

    node_output = results.get("ROS 2 Nodes", "")
    topic_output = results.get("ROS 2 Topics", "")

    node_status_known = (
        bool(node_output.strip())
        and "inconclusive" not in node_output.lower()
        and "(no results)" not in node_output.lower()
        and "command failed" not in node_output.lower()
        and "timed out" not in node_output.lower()
    )

    topic_status_known = (
        bool(topic_output.strip())
        and "(no results)" not in topic_output.lower()
        and "command failed" not in topic_output.lower()
        and "timed out" not in topic_output.lower()
    )

    actual_nodes = entries(node_output)
    actual_topics = entries(topic_output)

    if node_status_known:
        for node in expected_nodes or []:
            if node not in actual_nodes:
                faults.append({
                    "type": "Missing Node",
                    "name": node,
                    "severity": "Warning",
                    "details": f"Expected node {node} was not detected.",
                })

    if topic_status_known:
        for topic in expected_topics or []:
            if topic not in actual_topics:
                faults.append({
                    "type": "Missing Topic",
                    "name": topic,
                    "severity": "Warning",
                    "details": f"Expected topic {topic} was not detected.",
                })

    return faults
