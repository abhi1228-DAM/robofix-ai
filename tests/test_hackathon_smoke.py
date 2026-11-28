import unittest

from fault_detector import detect_faults
from command_validator import extract_commands, validate_command


class FaultDetectorTests(unittest.TestCase):

    def test_missing_resources_are_detected(self):
        results = {
            "ROS 2 Nodes": "/talker",
            "ROS 2 Topics": "/chatter\n/rosout"
        }

        faults = detect_faults(
            results,
            expected_nodes=["/talker", "/robot_controller"],
            expected_topics=["/chatter", "/imu"]
        )

        detected = {
            (fault["type"], fault["name"])
            for fault in faults
        }

        self.assertEqual(
            detected,
            {
                ("Missing Node", "/robot_controller"),
                ("Missing Topic", "/imu")
            }
        )

    def test_available_resources_produce_no_faults(self):
        results = {
            "ROS 2 Nodes": "/talker\n/robot_controller",
            "ROS 2 Topics": "/chatter\n/imu"
        }

        faults = detect_faults(
            results,
            expected_nodes=["/talker", "/robot_controller"],
            expected_topics=["/chatter", "/imu"]
        )

        self.assertEqual(faults, [])


class CommandValidatorTests(unittest.TestCase):

    def test_read_only_ros_command_is_recognized(self):
        valid, _ = validate_command("ros2 topic list")
        self.assertTrue(valid)

    def test_unsupported_command_is_rejected(self):
        valid, _ = validate_command("ros2 topic pub /imu")
        self.assertFalse(valid)

    def test_shell_operator_is_rejected(self):
        valid, _ = validate_command(
            "ros2 topic list && echo test"
        )
        self.assertFalse(valid)

    def test_ros_command_extraction(self):
        commands = extract_commands(
            "Suggested check:\n- ros2 node list\n"
        )
        self.assertEqual(commands, ["ros2 node list"])


if __name__ == "__main__":
    unittest.main()
