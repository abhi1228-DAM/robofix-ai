import streamlit as st

st.set_page_config(
    page_title="RoboFix AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RoboFix AI")
st.subheader("Intelligent ROS 2 Troubleshooting Assistant")

st.write(
    "Analyze robotics errors and discover "
    "possible solutions."
)

logs = st.text_area(
    "Paste your ROS 2 terminal errors",
    height=200,
    placeholder="Paste your error logs here..."
)

if st.button("Analyze Error"):
    if not logs.strip():
        st.warning("Please enter a ROS 2 error.")
    else:
        st.subheader("Diagnostic Result")
        text = logs.lower()

        if "not published yet" in text:
            st.error("ROS topic is not publishing.")
            st.info(
                "Check whether the sensor, node, "
                "or simulation bridge is running."
            )
            st.code("ros2 topic list")

        elif "command not found" in text:
            st.error("A required command is unavailable.")
            st.info(
                "Check the installation and "
                "environment configuration."
            )

        elif "package not found" in text:
            st.error("ROS package could not be located.")
            st.info(
                "Check package installation and "
                "source the ROS environment."
            )

        else:
            st.warning(
                "Unknown error. Additional "
                "diagnostic analysis is needed."
            )

st.divider()
st.caption("Developed by Abhilash B | Homingo Hack Days 2026")
