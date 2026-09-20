import pytest
from wpilib.simulation import SimDeviceSim

import navx


def test_get_angle():
    imu = navx.AHRS.create_spi()
    imu.getAngle()


def test_get_rotation2d():
    imu = navx.AHRS.create_spi()
    imu.getRotation2d()


def test_get_board_yaw_axis():
    imu = navx.AHRS.create_spi()
    imu.getBoardYawAxis()


def test_get_velocity_x():
    imu = navx.AHRS.create_spi()
    imu.getVelocityX()


@pytest.mark.parametrize("device_id", [0, 2, 3])
@pytest.mark.parametrize("update_rate", [None, 50])
@pytest.mark.parametrize("use_keywords", [False, True])
def test_navx_can_constructors(device_id, update_rate, use_keywords):
    if use_keywords:
        if update_rate is None:
            imu = navx.Navx(deviceId=device_id)
        else:
            imu = navx.Navx(deviceId=device_id, updateRate=update_rate)
    elif update_rate is None:
        imu = navx.Navx(device_id)
    else:
        imu = navx.Navx(device_id, update_rate)

    sim = SimDeviceSim(f"NavX3[{device_id}]")
    sim.getDouble("Yaw").set(42.5)
    assert imu.getYaw() == pytest.approx(42.5)


@pytest.mark.parametrize(
    "port, sim_name",
    [(navx.Navx.Port.kUSB1, "NavX3[2]"), (navx.Navx.Port.kUSB2, "NavX3[3]")],
)
@pytest.mark.parametrize("update_rate", [None, 50])
@pytest.mark.parametrize("use_keywords", [False, True])
def test_navx_usb_constructors(port, sim_name, update_rate, use_keywords, monkeypatch):
    # CAN ID 2/3 and USB port 2/3 have identical simulation device names.
    # Observe integer coercion without changing it: choosing the CAN overload
    # would call __index__, whereas the USB overload accepts the enum directly.
    integer_conversions = []
    original_index = navx.Navx.Port.__index__

    def track_index(value):
        integer_conversions.append(value)
        return original_index(value)

    monkeypatch.setattr(navx.Navx.Port, "__index__", track_index)

    if use_keywords:
        if update_rate is None:
            imu = navx.Navx(port=port)
        else:
            imu = navx.Navx(port=port, updateRate=update_rate)
    elif update_rate is None:
        imu = navx.Navx(port)
    else:
        imu = navx.Navx(port, update_rate)

    assert integer_conversions == []

    sim = SimDeviceSim(sim_name)
    sim.getDouble("Yaw").set(42.5)
    sim.getDouble("Angle").set(402.5)

    assert imu.getYaw() == pytest.approx(42.5)
    assert imu.getAngle() == pytest.approx(402.5)

    error, rotation = imu.getRotation2D()
    assert error is False
    assert rotation.degrees() == pytest.approx(42.5)


@pytest.mark.parametrize("enable", [False, True])
def test_navx_enable_9d_yaw(enable):
    imu = navx.Navx(navx.Navx.Port.kUSB1)
    # Studica returns False on success, not True.
    assert imu.enable9DYaw(enable) is False


def test_navx_optional_angle_messages():
    imu = navx.Navx(0)
    assert (
        imu.enableOptionalMessages(
            yaw=True,
            angle=True,
            quat6d=False,
            quat9d=False,
            algoStates=False,
            pitchRoll=False,
            angularVel=False,
            linearAccel=False,
            compass=False,
            temperature=False,
        )
        is False
    )
