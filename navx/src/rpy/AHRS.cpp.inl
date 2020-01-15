cls_AHRS.def_static("create_spi", [](
    frc::SPI::Port port,
    uint32_t bitrate,
    uint8_t update_rate_hz
    ) -> std::shared_ptr<AHRS> {
        return std::make_shared<AHRS>(port, bitrate, update_rate_hz);
    },
    py::arg("port") = frc::SPI::Port::kMXP,
    py::arg("bitrate") =500000, // DEFAULT_SPI_BITRATE in AHRS.cpp
    py::arg("update_rate_hz") = 60, // NAVX_DEFAULT_UPDATE_RATE_HZ
    release_gil(),
    "Constructs the AHRS class using SPI communication, overriding the\n"
    "default update rate with a custom rate which may be from 4 to 100,\n"
    "representing the number of updates per second sent by the sensor.\n\n"
    "This constructor allows the specification of a custom SPI bitrate, in bits/second.\n\n"
    ".. note:: Increasing the update rate may increase the CPU utilization.\n\n"
    ":param port: SPI Port to use\n"
    ":type port: :class:`.SPI.Port`\n"
    ":param spi_bitrate: SPI bitrate (Maximum:  2,000,000)\n"
    ":param update_rate_hz: Custom Update Rate (Hz)");

cls_AHRS.def_static("create_i2c", [](
    frc::I2C::Port port,
    uint8_t update_rate_hz
    ) -> std::shared_ptr<AHRS> {
        return std::make_shared<AHRS>(port, update_rate_hz);
    },
    py::arg("port") = frc::I2C::Port::kMXP,
    py::arg("update_rate_hz") = 60, // NAVX_DEFAULT_UPDATE_RATE_HZ
    release_gil(),
    "Constructs the AHRS class using I2C communication, overriding the "
    "default update rate with a custom rate which may be from 4 to 100, "
    "representing the number of updates per second sent by the sensor.\n\n"
    "This constructor should be used if communicating via I2C.\n\n"
    ".. note:: Increasing the update rate may increase the CPU utilization.\n\n"
    ":param port: I2C Port to use\n"
    ":type port: :class:`.I2C.Port` "
    ":param update_rate_hz: Custom Update Rate (Hz)\n");