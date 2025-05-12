import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ROS settings
ROSBRIDGE_WS_URL = os.getenv("ROSBRIDGE_WS_URL", "ws://10.4.89.73:9090")

# Whisper model settings
WHISPER_MODEL_TYPE = os.getenv("WHISPER_MODEL_TYPE", "base")

# NLP model settings
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
