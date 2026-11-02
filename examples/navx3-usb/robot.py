#!/usr/bin/env python3
"""Publish NavX3 USB readings with RobotPy 2027."""

import navx
import wpilib
from ntcore import NetworkTableInstance


class MyRobot(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()
        self.table = NetworkTableInstance.get_default().get_table("NavX3")
        self.imu = navx.Navx.usb()  # Discover a single sensor on any USB port
        # For multiple sensors, select a SystemCore port for each:
        # self.imu = navx.Navx.usb(navx.UsbPort.USB1, updateRateHz=50)
        # Or select an explicit serial device:
        # self.imu = navx.Navx.fromSerialDevice("/dev/ttyACM0")

    def robot_periodic(self):
        self.table.put_boolean("Connected", self.imu.isConnected())
        # Yaw is wrapped to +/-180 degrees; angle is continuous.
        for name, reading in (
            ("Yaw", self.imu.getYaw()),
            ("Angle", self.imu.getAngle()),
        ):
            # Getters return None while data is missing, disabled, or stale.
            self.table.put_boolean(f"{name}Valid", reading is not None)
            self.table.put_number(
                name, reading if reading is not None else float("nan")
            )


if __name__ == "__main__":
    wpilib.TimedRobot.main(MyRobot)
