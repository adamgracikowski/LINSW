import os

# LEDs
LED_GREEN_PIN = int(os.getenv("LED_GREEN_PIN", 22))
LED_YELLOW_PIN = int(os.getenv("LED_YELLOW_PIN", 23))
LED_RED_PIN = int(os.getenv("LED_RED_PIN", 27))

# Buttons
BUTTON_A_PIN = int(os.getenv("BUTTON_A_PIN", 25))
BUTTON_B_PIN = int(os.getenv("BUTTON_B_PIN", 10))
BUTTON_C_PIN = int(os.getenv("BUTTON_C_PIN", 17))
BUTTON_FAILURE_PIN = int(os.getenv("BUTTON_FAILURE_PIN", 18))

# Database
DATABASE_URL = "sqlite:///production.db"

# Web Server
SERVER_HOST = os.getenv("SERVER_HOST", "192.168.145.221")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8881))

WS_ENDPOINT = os.getenv("WS_ENDPOINT", "/ws")
UI_ENDPOINT = os.getenv("UI_ENDPOINT", "/ui")

# Authentication

USERNAME = os.getenv("USERNAME", "adam")
PASSWORD = os.getenv("PASSWORD", "secret")

TEMPLATES = os.getenv("TEMPLATES", "templates")

# Logging
LOG_FILE = os.getenv("LOG_FILE", "logs/events.log")