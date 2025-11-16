import time
import requests
from abc import ABC, abstractmethod
from typing import Dict

from app.core.config import settings


class GateController(ABC):
    @abstractmethod
    def open(self) -> bool:
        """Open the gate"""
        pass

    @abstractmethod
    def close(self) -> bool:
        """Close the gate"""
        pass

    @abstractmethod
    def get_status(self) -> Dict:
        """Get gate status"""
        pass


class MockGateController(GateController):
    """Mock gate controller for testing"""

    def __init__(self):
        self.is_open = False

    def open(self) -> bool:
        print("MOCK: Opening gate")
        self.is_open = True
        return True

    def close(self) -> bool:
        print("MOCK: Closing gate")
        self.is_open = False
        return True

    def get_status(self) -> Dict:
        return {
            "is_open": self.is_open,
            "type": "mock"
        }


class HTTPRelayController(GateController):
    """HTTP-based relay controller"""

    def __init__(self):
        self.base_url = f"http://{settings.GATE_CONTROLLER_HOST}:{settings.GATE_CONTROLLER_PORT}"
        self.is_open = False

    def open(self) -> bool:
        try:
            # Adjust endpoint based on your relay device's API
            response = requests.get(f"{self.base_url}/relay/on")
            if response.status_code == 200:
                self.is_open = True
                return True
            return False
        except Exception as e:
            print(f"Error opening gate: {e}")
            return False

    def close(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/relay/off")
            if response.status_code == 200:
                self.is_open = False
                return True
            return False
        except Exception as e:
            print(f"Error closing gate: {e}")
            return False

    def get_status(self) -> Dict:
        return {
            "is_open": self.is_open,
            "type": "http_relay"
        }


class SerialRelayController(GateController):
    """Serial port-based relay controller"""

    def __init__(self):
        try:
            import serial
            self.serial = serial.Serial(
                settings.GATE_CONTROLLER_SERIAL_PORT,
                settings.GATE_CONTROLLER_BAUD_RATE
            )
            self.is_open = False
        except Exception as e:
            print(f"Error initializing serial connection: {e}")
            self.serial = None

    def open(self) -> bool:
        if not self.serial:
            return False

        try:
            # Send command to open relay (adjust based on your relay)
            self.serial.write(b'OPEN\n')
            self.is_open = True
            return True
        except Exception as e:
            print(f"Error opening gate: {e}")
            return False

    def close(self) -> bool:
        if not self.serial:
            return False

        try:
            self.serial.write(b'CLOSE\n')
            self.is_open = False
            return True
        except Exception as e:
            print(f"Error closing gate: {e}")
            return False

    def get_status(self) -> Dict:
        return {
            "is_open": self.is_open,
            "type": "serial_relay",
            "connected": self.serial is not None
        }


def get_gate_controller() -> GateController:
    """Factory function to get appropriate gate controller"""
    controller_type = settings.GATE_CONTROLLER_TYPE.lower()

    if controller_type == "http":
        return HTTPRelayController()
    elif controller_type == "serial":
        return SerialRelayController()
    else:  # mock or any other value
        return MockGateController()


# Singleton instance
gate_controller = get_gate_controller()
