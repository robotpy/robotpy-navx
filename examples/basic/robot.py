#!/usr/bin/env python3
"""Publish NavX3 CAN readings with RobotPy 2027."""

import navx
import wpilib
from ntcore import NetworkTableInstance


class MyRobot(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()
        self.table = NetworkTableInstance.get_default().get_table("NavX3")
        # Match the configured CAN device ID and SystemCore bus.
        self.imu = navx.Navx(0, bus=wpilib.CANPort.CAN_S0, updateRateHz=100)

    def robot_periodic(self):
        self.table.put_boolean("Connected", self.imu.isConnected())
        for name, reading in (
            ("Yaw", self.imu.getYaw()),
            ("Angle", self.imu.getAngle()),
            ("Pitch", self.imu.getPitch()),
            ("Roll", self.imu.getRoll()),
            ("Timestamp", self.imu.getTimestamp()),
        ):
            # Missing/stale readings are None, not zero. Clear old telemetry
            # with NaN and publish validity separately for dashboard consumers.
            self.table.put_boolean(f"{name}Valid", reading is not None)
            self.table.put_number(
                name, reading if reading is not None else float("nan")
            )


if __name__ == "__main__":
    wpilib.TimedRobot.main(MyRobot)
