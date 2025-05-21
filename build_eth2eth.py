#!/usr/bin/env python3
from migen import *
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.builder  import Builder
from board import TangNano35KPlatform

# Import basic modules
from liteeth.mac import LiteEthMAC
from litex.soc.interconnect import stream

# Custom RGMII PHY Implementation
class RGMIIMAC(Module):
    def __init__(self, pads, clk_freq=int(50e6)):
        self.pads = pads
        
        # Clock domain for RGMII RX
        self.clock_domains.cd_eth_rx = ClockDomain()
        self.comb += self.cd_eth_rx.clk.eq(pads.rx_clk)
        
        # Source and Sink
        self.source = stream.Endpoint([("data", 8)])
        self.sink = stream.Endpoint([("data", 8)])
        
        # Simple connection for RX data to source
        rx_data = Signal(4)
        rx_ctl = Signal()
        
        self.specials += [
            Instance("IODELAY",
                i_D=pads.rx_data,
                o_Q=rx_data
            ),
            Instance("IODELAY",
                i_D=pads.rx_ctl,
                o_Q=rx_ctl
            )
        ]
        
        # Convert 4-bit data to byte stream
        self.sync.eth_rx += [
            If(rx_ctl,
                self.source.valid.eq(1),
                self.source.data.eq(Cat(rx_data, rx_data))
            ).Else(
                self.source.valid.eq(0)
            )
        ]
        
        # TX side
        tx_data = Signal(4)
        tx_ctl = Signal()
        
        # Clock domain for RGMII TX
        tx_clk = Signal()
        self.specials += Instance("CLKDIV",
            p_DIV_MODE="2",
            i_RESET=0,
            i_HCLKIN=ClockSignal(),
            o_CLKOUT=tx_clk
        )
        
        # Simple connection from sink to TX data
        self.sync += [
            If(self.sink.valid & self.sink.ready,
                tx_data.eq(self.sink.data[:4]),
                tx_ctl.eq(1)
            ).Else(
                tx_ctl.eq(0)
            ),
            self.sink.ready.eq(1)
        ]
        
        # Output to pads
        self.specials += [
            Instance("IOBUF",
                i_I=tx_data,
                o_O=pads.tx_data
            ),
            Instance("IOBUF",
                i_I=tx_ctl,
                o_O=pads.tx_ctl
            ),
            Instance("IOBUF",
                i_I=tx_clk,
                o_O=pads.tx_clk
            )
        ]

class Eth2EthSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(50e6)):
        # 1) Create the platform
        platform = TangNano35KPlatform()

        # 2) Instantiate a bare-bones SoC (no CPU, no RAM)
        SoCCore.__init__(self, platform,
            clk_freq=sys_clk_freq,
            cpu_type=None,
            integrated_main_ram_size=0,
            ident="Ethernet Bridge", ident_version=True
        )

        # 3) Create custom RGMII PHYs
        self.submodules.phy1 = RGMIIMAC(
            platform.request("eth_e1"),
            clk_freq=sys_clk_freq
        )
        self.submodules.phy2 = RGMIIMAC(
            platform.request("eth_e2"),
            clk_freq=sys_clk_freq
        )

        # 4) Connect PHYs with FIFO buffers
        self.submodules.fifo1 = stream.SyncFIFO(
            [("data", 8)],
            depth=2048,
            buffered=True
        )
        self.submodules.fifo2 = stream.SyncFIFO(
            [("data", 8)],
            depth=2048,
            buffered=True
        )

        # Connect PHY1 to FIFO1 to PHY2
        self.comb += [
            self.phy1.source.connect(self.fifo1.sink),
            self.fifo1.source.connect(self.phy2.sink)
        ]

        # Connect PHY2 to FIFO2 to PHY1
        self.comb += [
            self.phy2.source.connect(self.fifo2.sink),
            self.fifo2.source.connect(self.phy1.sink)
        ]

if __name__ == "__main__":
    soc = Eth2EthSoC()
    builder = Builder(soc, output_dir="build")
    builder.build(run=True)