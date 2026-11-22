# RoboFix AI

**Local AI-Powered ROS 2 Troubleshooting Assistant**

Developed by Abhilash B for Homingo Hack Days 2026.

## Overview

RoboFix AI helps robotics developers diagnose
ROS 2 problems using local artificial intelligence,
live system diagnostics, and fault detection.

## Features

- ROS 2 error log analysis
- Live Docker-based ROS 2 diagnostics
- Missing node and topic detection
- Local AI analysis using Ollama
- Basic validation of suggested ROS 2 commands
- Downloadable diagnostic reports

## Technology Stack

Python, Streamlit, ROS 2 Humble, Docker,
Ollama, and Qwen 2.5 3B.

## Installation

1. Clone this repository.
2. Create a Python virtual environment:

       python3 -m venv .venv
       source .venv/bin/activate

3. Install Python dependencies:

       python3 -m pip install -r requirements.txt

4. Install Ollama separately and download the model:

       ollama pull qwen2.5:3b

5. Make sure Ollama and Docker are running.

## Run RoboFix AI

    python3 -m streamlit run app.py --server.port 8765

Open http://127.0.0.1:8765/

## ROS 2 Environment

The current live diagnostics integration uses
a Docker container named `autofleet-desktop`
with ROS 2 Humble installed.

## Tested Features

- /talker node discovery
- /chatter topic discovery
- Missing /imu topic warning
- Local AI diagnostic analysis
- AI command validation interface
- Markdown diagnostic report export

## Limitations

This is an educational diagnostic prototype.
AI recommendations may be inaccurate and
should be reviewed before use.

The application does not automatically repair
robots or execute AI-generated commands.

## Developer

Abhilash B

GitHub: https://github.com/abhi1228-DAM
