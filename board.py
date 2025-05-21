from litex.build.generic_platform import *
from litex.build.gowin import GowinPlatform

# Define the IOs for the Ethernet PHY
_io = [
    # Ethernet PHY E1 (J2 connector)
    ("eth_e1", 0,
        Subsignal("tx_clk", Pins("F2")),
        Subsignal("tx_ctl", Pins("F1")),
        Subsignal("tx_data", Pins("A1 D8 E1 D1")),
        Subsignal("rx_clk", Pins("L2")),
        Subsignal("rx_ctl", Pins("L1")),
        Subsignal("rx_data", Pins("K1 K2 B2 C2")),
        Subsignal("mdio", Pins("K7")),
        Subsignal("mdc", Pins("J7")),
        IOStandard("LVCMOS33")
    ),

    # Ethernet PHY E2 (J1 connector)
    ("eth_e2", 0,
        Subsignal("tx_clk", Pins("H5")),
        Subsignal("tx_ctl", Pins("J5")),
        Subsignal("tx_data", Pins("L5 K5 H8 H7")),
        Subsignal("rx_clk", Pins("L6")),
        Subsignal("rx_ctl", Pins("K6")),
        Subsignal("rx_data", Pins("G7 G8 F5 G5")),
        Subsignal("mdio", Pins("K7")),
        Subsignal("mdc", Pins("J7")),
        IOStandard("LVCMOS33")
    ),
]

# Define the platform
class TangNano25KPlatform(GowinPlatform):
    def __init__(self):
        GowinPlatform.__init__(self, "GW2A-LV18QN88C8/I6", _io)
