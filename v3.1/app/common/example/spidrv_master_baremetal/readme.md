# SPI Master Baremetal application #

This example project demonstrates use of the Serial Peripheral Interface in master mode 
in a bare-metal configuration.

Once the master application is installed on a starter kit, the kit can be connected 
via the 20-pint expansion header to a second kit which has the slave application installed.

The expansion header pins must be connected as the following:
Connect master CS to slave CS
Connect master SCLK to slave SCLK
Connect master MOSI to slave MOSI
Connect master MISO to slave MISO

The user can then connect to the device via the VCOM serial connection. The master and slave
devices will periodically exchange data, logging the exchanges over VCOM.
