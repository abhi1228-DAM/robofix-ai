def detect_faults(results, expected_nodes=None, expected_topics=None):
    faults = []

    node_output = results.get("ROS 2 Nodes", "")
    topic_output = results.get("ROS 2 Topics", "")

    def entries(output):
        return {
            line.strip()
            for line in output.splitlines()
            if line.strip().startswith("/")
        }

    actual_nodes = entries(node_output)
    actual_topics = entries(topic_output)

    for node in expected_nodes or []:
        if node not in actual_nodes:
            faults.append({
                "type": "Missing Node",
                "name": node,
                "severity": "Warning",
                "details": f"Expected node {node} was not detected."
            })

    for topic in expected_topics or []:
        if topic not in actual_topics:
            faults.append({
                "type": "Missing Topic",
                "name": topic,
                "severity": "Warning",
                "details": f"Expected topic {topic} was not detected."
            })

    return faults
