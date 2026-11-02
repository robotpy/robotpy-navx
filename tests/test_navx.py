import time

import pytest
import wpilib
from wpilib.simulation import SimDeviceSim

import navx


def wait_for(predicate):
    """Wait for Studica's background reader to publish a simulation update."""
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.005)
    assert predicate(), "NavX simulation did not publish the expected update"


@pytest.mark.parametrize("use_keywords", [False, True])
@pytest.mark.parametrize("can_id", [0, 2, 3])
def test_can_constructors(can_id, use_keywords):
    if use_keywords:
        imu = navx.Navx(canId=can_id, bus=wpilib.CANPort.CAN_S0, updateRateHz=50)
    else:
        imu = navx.Navx(can_id, wpilib.CANPort.CAN_S0, 50)
    assert imu.isOpen()
    sim = SimDeviceSim(f"NavX3[{can_id}]")
    sim.get_double("Yaw").set(42.5)
    sim.get_double("Angle").set(402.5)
    wait_for(lambda: imu.getYaw() == 42.5 and imu.getAngle() == 402.5)
    assert imu.getRotation2d().degrees() == pytest.approx(42.5)


@pytest.mark.parametrize("port", list(navx.UsbPort.__members__.values()))
@pytest.mark.parametrize("use_keywords", [False, True])
@pytest.mark.parametrize("update_rate", [None, 50])
def test_usb_port_overload(port, use_keywords, update_rate):
    if use_keywords:
        kwargs = {} if update_rate is None else {"updateRateHz": update_rate}
        imu = navx.Navx.usb(port=port, **kwargs)
    elif update_rate is None:
        imu = navx.Navx.usb(port)
    else:
        imu = navx.Navx.usb(port, update_rate)
    # The integer overload instead opens USB-any and treats the port as a rate.
    sim_name = f"NavX3[USB port {port.value}]"
    assert sim_name in SimDeviceSim.enumerate_devices()
    SimDeviceSim(sim_name).get_double("Yaw").set(-12.5)
    wait_for(lambda: imu.getYaw() == -12.5)


@pytest.mark.parametrize("update_rate", [None, 50])
def test_usb_any(update_rate):
    imu = navx.Navx.usb() if update_rate is None else navx.Navx.usb(update_rate)
    SimDeviceSim("NavX3[USB]").get_double("Yaw").set(21.0)
    wait_for(lambda: imu.getYaw() == 21.0)


def test_serial_device():
    imu = navx.Navx.fromSerialDevice("/dev/robotpy-test-navx", updateRateHz=50)
    SimDeviceSim("NavX3[/dev/robotpy-test-navx]").get_double("Yaw").set(15.0)
    wait_for(lambda: imu.getYaw() == 15.0)


def test_message_flags():
    messages = navx.NavxMessage.YAW | navx.NavxMessage.ANGLE
    assert isinstance(messages, navx.NavxMessage)
    assert messages.value == 5
    imu = navx.Navx(0)
    assert imu.enableMessages(messages) == navx.Status.OK


def test_sensor_readings():
    imu = navx.Navx(0)
    sim = SimDeviceSim("NavX3[0]")
    sim.get_double("Pitch").set(12.0)
    sim.get_double("Roll").set(-8.0)
    sim.get_double("Angular Velocity X").set(1.5)
    sim.get_double("Acceleration Y").set(2.5)
    sim.get_double("Compass Norm").set(35.0)
    sim.get_double("Temperature").set(26.0)
    wait_for(lambda: imu.getTemperature() == 26.0)
    assert imu.getPitch() == 12.0
    assert imu.getRoll() == -8.0
    assert imu.getAngularVelocity().x == 1.5
    assert imu.getLinearAcceleration().y == 2.5
    assert imu.getMagneticField().norm == 35.0
    assert isinstance(imu.getAlgorithmState(), navx.AlgorithmState)
    assert imu.getQuaternion6d().w == 1.0
    assert imu.getQuaternion9d().w == 1.0
    assert imu.getRotation3d().x == 0.0
    assert isinstance(imu.getTimestamp(), float)
    assert isinstance(imu.isTimeSynced(), bool)


@pytest.mark.parametrize("method", ["getFirmwareVersion", "getSensorUuid", "selfTest"])
def test_expected_results_on_invalid_device(method):
    imu = navx.Navx(-1)
    assert getattr(imu, method)() == (navx.Status.INVALID_HANDLE, None)


def test_firmware_version():
    imu = navx.Navx(0)
    status, firmware = imu.getFirmwareVersion()
    assert status == navx.Status.OK
    assert isinstance(firmware, navx.FirmwareVersion)
    assert (firmware.major, firmware.minor, firmware.patch) == (0, 0, 0)


def test_sensor_uuid():
    imu = navx.Navx(0)
    assert imu.getSensorUuid() == (navx.Status.OK, [0, 0, 0])


def test_self_test():
    imu = navx.Navx(0)
    status, result = imu.selfTest()
    assert status == navx.Status.OK
    assert isinstance(result, navx.SelfTestResult)
    assert result.gyro == 1
    assert result.gyroAxes == [1, 1, 1]
    assert result.accel == 1
    assert result.accelAxes == [1, 1, 1]


@pytest.mark.parametrize(
    "method",
    [
        "getYaw",
        "getPitch",
        "getRoll",
        "getAngle",
        "getRotation2d",
        "getRotation3d",
        "getQuaternion6d",
        "getQuaternion9d",
        "getAngularVelocity",
        "getLinearAcceleration",
        "getMagneticField",
        "getAlgorithmState",
        "getTemperature",
        "getTimestamp",
    ],
)
def test_unavailable_readings(method):
    imu = navx.Navx(-1)
    assert not imu.isOpen()
    assert not imu.isConnected()
    assert not imu.isTimeSynced()
    assert getattr(imu, method)() is None


def test_commands():
    imu = navx.Navx(0)
    assert imu.resetYaw() == navx.Status.OK
    assert imu.setOutputRate(50) == navx.Status.OK
    assert imu.use9AxisYaw(True) == navx.Status.OK
    assert imu.use9AxisYaw(False) == navx.Status.OK
    assert imu.setOutputRate(0) == navx.Status.INVALID_ARGUMENT


def test_can_bus():
    for mode in (navx.CanBusMode.FD_5MBPS, navx.CanBusMode.CLASSIC):
        assert (
            navx.CanBus.requestMode(wpilib.CANPort.CAN_S0, mode, 0.0) == navx.Status.OK
        )
        assert navx.CanBus.getMode(wpilib.CANPort.CAN_S0) == mode
