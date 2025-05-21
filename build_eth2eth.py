#!/usr/bin/env python3
from migen import *
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.builder  import Builder
from board import TangNano25KPlatform

# PHY + switch imports
#from liteeth.phy.rgmii    import LiteEthPHYRGMI
from liteeth.phy.gw5rgmii import LiteEthPHYGW5RGMI
from liteeth.crossbar     import LiteEthCrossbar

class Eth2EthSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(50e6)):
        # 1) Create the platform
        platform = TangNano25KPlatform()

        # 2) Instantiate a bare‐bones SoC (no CPU, no RAM)
        SoCCore.__init__(self, platform,
            clk_freq=sys_clk_freq,
            cpu_type=None,
            integrated_main_ram_size=0,
            ident="Ethernet Bridge", ident_version=True
        )

        # 3) Add two RGMII PHYs on our connectors
        self.submodules.phy1 = LiteEthPHYRGMI(
            platform.request("eth_e1"),
            clk_freq=sys_clk_freq
        )
        self.submodules.phy2 = LiteEthPHYRGMI(
            platform.request("eth_e2"),
            clk_freq=sys_clk_freq
        )

        # 4) Instantiate the crossbar to forward frames between them
        self.submodules.bridge = LiteEthCrossbar(
            phys=[self.phy1, self.phy2]
        )

if __name__ == "__main__":
    soc     = Eth2EthSoC()
    builder = Builder(soc, output_dir="build")
    builder.build(run=True)