from litex.build.generic_platform import *
from litex.build.gowin.platform import GowinPlatform

# Define the IOs for the Ethernet PHY
_io = [
    # Ethernet PHY E1 (J2 connector)
    ("eth_e1", 0,
        Subsignal("tx_clk", Pins("F2_IOB26A_40P")),
        Subsignal("tx_ctl", Pins("F1_IOB26B_40P")),
        Subsignal("tx_data", Pins("A1_IOB24A_40P D8_RECONFIG E1_IOB12B_40P D1_IOB14B_40P")),
        Subsignal("rx_clk", Pins("L2_IOR18A_40P")),
        Subsignal("rx_ctl", Pins("L1_IOR18B_40P")),
        Subsignal("rx_data", Pins("K1_IOR20A_40P K2_IOR20B_40P B2_IOB4A_40P C2_IOB4B_40P")),
        Subsignal("mdio", Pins("K7_IOT21A_40P")),
        Subsignal("mdc", Pins("J7_IOT21B_40P")),
        IOStandard("LVCMOS33")
    ),

    # Ethernet PHY E2 (J1 connector)
    ("eth_e2", 0,
        Subsignal("tx_clk", Pins("H5_IOT61A")),
        Subsignal("tx_ctl", Pins("J5_IOT61B")),
        Subsignal("tx_data", Pins("L5_IOT63A K5_IOT63B H8_IOT66A H7_IOT66B")),
        Subsignal("rx_clk", Pins("L6_IOT23A_USB_P")),
        Subsignal("rx_ctl", Pins("K6_IOT23B_USB_N")),
        Subsignal("rx_data", Pins("G7_IOT68A G8_IOT68B F5_IOT72A G5_IOT72B")),
        Subsignal("mdio", Pins("K7_IOT21A_40P")),
        Subsignal("mdc", Pins("J7_IOT21B_40P")),
        IOStandard("LVCMOS33")
    ),
]

# Define the platform
class TangNano35KPlatform(GowinPlatform):
    def __init__(self):
        GowinPlatform.__init__(self, "GW5A-25", _io)
