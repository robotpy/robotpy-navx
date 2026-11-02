NavX API
========

This package is not installed on the robot by default. These bindings use
StudicaLib 2027.0.0-alpha-1 and require RobotPy 2027.

Opening a NavX3
---------------

Choose one connection per device:

.. code-block:: python

    import navx
    import wpilib

    imu = navx.Navx(0, bus=wpilib.CANPort.CAN_S0, updateRateHz=100)
    # Alternatively, use one of these USB constructors:
    # imu = navx.Navx.usb()
    # imu = navx.Navx.usb(navx.UsbPort.USB1, updateRateHz=50)
    # imu = navx.Navx.fromSerialDevice("/dev/ttyACM0")

CAN defaults to ``CAN_S0`` and 100 Hz. All constructors accept an update rate
of 1–200 Hz. ``UsbPort`` names (``USB0`` through ``USB3``) match the SystemCore
labels. With multiple USB sensors, select a port for each instead of using
automatic discovery.

``isOpen()`` reports whether opening succeeded; ``isConnected()`` reports recent
data. If opening fails, getters return ``None`` and commands return
``Status.INVALID_HANDLE``. Legacy SPI/I2C interfaces are no longer supported.

Readings and commands
---------------------

Readings arrive in the background. Optional getters return a value or ``None``
if their message group is disabled, missing, or stale; there are no numeric
error sentinels or error-flag tuples for these getters.

.. code-block:: python

    yaw = imu.getYaw()      # degrees, typically -180 to 180
    angle = imu.getAngle()  # continuous degrees
    rotation = imu.getRotation2d()
    if yaw is not None:
        print("Yaw:", yaw)
    if angle is not None:
        print("Angle:", angle)
    if rotation is not None:
        print("Heading:", rotation.degrees())

Other readings include ``getRotation3d()``, ``getQuaternion6d()``,
``getQuaternion9d()``, ``getAngularVelocity()`` (rad/s),
``getLinearAcceleration()`` (m/s²), ``getMagneticField()`` (microtesla),
``getAlgorithmState()``, and ``getTemperature()`` (Celsius).
``getTimestamp()`` returns seconds on the WPILib timer clock, or ``None``.
``isTimeSynced()`` distinguishes sensor measurement times from arrival times.

Commands such as ``resetYaw()``, ``setOutputRate()``, ``enableMessages()``, and
``use9AxisYaw()`` return a ``Status`` enum, not an error boolean:

.. code-block:: python

    status = imu.resetYaw()
    if status != navx.Status.OK:
        print("Reset failed:", status)

    # Only these groups will stream; other readings will return None.
    status = imu.enableMessages(navx.NavxMessage.YAW | navx.NavxMessage.ANGLE)
    if status != navx.Status.OK:
        print("Stream configuration failed:", status)

``getFirmwareVersion()``, ``getSensorUuid()``, and ``selfTest()`` return
``(Status, value_or_None)``:

.. code-block:: python

    status, version = imu.getFirmwareVersion()
    if status == navx.Status.OK and version is not None:
        print(f"{version.major}.{version.minor}.{version.patch}")
    else:
        print("Firmware query failed:", status)

The sensor UUID contains three 32-bit integers. ``selfTest()`` returns a
``SelfTestResult``; it blocks for several seconds and interrupts sensor data.
Keep the robot still and do not run it in a periodic control loop.

CAN bus configuration
---------------------

``CanBus.requestMode(port, mode, timeout=3.0)`` returns ``Status``.
Call it once at startup, before opening devices, if you need to switch between
``CanBusMode.CLASSIC`` and ``CanBusMode.FD_5MBPS``. Switching briefly interrupts
the entire bus; every device on an FD bus must support CAN FD.
``CanBus.getMode(port)`` returns a ``CanBusMode`` or ``None`` if unknown.

API reference
-------------

.. autoclass:: navx.Navx
    :members:
    :undoc-members:

.. autoclass:: navx.NavxMessage
    :members:
    :undoc-members:

.. autoclass:: navx.UsbPort
    :members:
    :undoc-members:

.. autoclass:: navx.Status
    :members:
    :undoc-members:

.. autoclass:: navx.FirmwareVersion
    :members:
    :undoc-members:

.. autoclass:: navx.AngularVelocity3d
    :members:
    :undoc-members:

.. autoclass:: navx.Acceleration3d
    :members:
    :undoc-members:

.. autoclass:: navx.MagneticField
    :members:
    :undoc-members:

.. autoclass:: navx.AlgorithmState
    :members:
    :undoc-members:

.. autoclass:: navx.SelfTestResult
    :members:
    :undoc-members:

.. autoclass:: navx.CanBus
    :members:
    :undoc-members:

.. autoclass:: navx.CanBusMode
    :members:
    :undoc-members:
