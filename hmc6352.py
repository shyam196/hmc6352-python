from __future__ import division # backport python3 division to python2
import smbus

class HMC6352:
    """
    Class for an HMC6352 digital compass

    Simple functionality -- does not implement anything except getting a heading from the device
    in "standby" mode (see datasheet -- this is the default mode of the device)

    Tested with Python 3.5

    Example usage:

    >>> bus = smbus.SMBus(1)
    >>> compass = HMC6352(0x21, bus)
    >>> print(compass.heading)
    """

    _READ_CMD = 0x41 # Command is "A"

    def __init__(self, address, bus):
        """
        Constructor for compass object

        :param address: The i2c address of the device (use `i2cdetect` on command line)
        :param bus: An instance of smbus.SMBus
        """
        self.bus = bus
        self.address = address

    @property
    def heading(self):
        """Returns the heading as a double (0.0 - 359.9)"""

        # Read two bytes off the bus once command sent; first byte MSBs, second LSBs
        data = self.bus.read_i2c_block_data(self.address, HMC6352._READ_CMD, 2)

        return ((data[0] << 8) + data[1]) / 10


if __name__ == "__main__":
    import time

    print("Testing HMC6352")

    bus = smbus.SMBus(1)
    compass = HMC6352(0x21, bus)

    while True:
        print(compass.heading)
        time.sleep(0.1)
