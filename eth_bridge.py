#!/usr/bin/env python3
from migen import *
from migen.genlib.fifo import SyncFIFO
from migen.fhdl import verilog
import os

class EthernetBridge(Module):
    def __init__(self):
        # Define clock domains
        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_eth1_rx = ClockDomain()
        self.clock_domains.cd_eth2_rx = ClockDomain()
        
        # Signals for ETH1
        self.eth1_rx_clk = Signal(name="eth1_rx_clk")
        self.eth1_rx_ctl = Signal(name="eth1_rx_ctl")
        self.eth1_rx_data = Signal(4, name="eth1_rx_data")
        self.eth1_tx_clk = Signal(name="eth1_tx_clk")
        self.eth1_tx_ctl = Signal(name="eth1_tx_ctl")
        self.eth1_tx_data = Signal(4, name="eth1_tx_data")
        
        # Signals for ETH2
        self.eth2_rx_clk = Signal(name="eth2_rx_clk")
        self.eth2_rx_ctl = Signal(name="eth2_rx_ctl")
        self.eth2_rx_data = Signal(4, name="eth2_rx_data")
        self.eth2_tx_clk = Signal(name="eth2_tx_clk")
        self.eth2_tx_ctl = Signal(name="eth2_tx_ctl")
        self.eth2_tx_data = Signal(4, name="eth2_tx_data")
        
        # Connect clock domains
        self.comb += [
            self.cd_eth1_rx.clk.eq(self.eth1_rx_clk),
            self.cd_eth2_rx.clk.eq(self.eth2_rx_clk)
        ]
        
        # Create FIFOs for data buffering
        eth1_to_eth2_fifo = SyncFIFO(width=4, depth=2048)
        eth2_to_eth1_fifo = SyncFIFO(width=4, depth=2048)
        self.submodules += eth1_to_eth2_fifo, eth2_to_eth1_fifo
        
        # ETH1 RX to ETH2 TX
        self.sync.eth1_rx += [
            If(self.eth1_rx_ctl,
               eth1_to_eth2_fifo.we.eq(1),
               eth1_to_eth2_fifo.din.eq(self.eth1_rx_data)
            ).Else(
               eth1_to_eth2_fifo.we.eq(0)
            )
        ]
        self.comb += [
            self.eth2_tx_data.eq(eth1_to_eth2_fifo.dout),
            self.eth2_tx_ctl.eq(~eth1_to_eth2_fifo.readable),
            eth1_to_eth2_fifo.re.eq(~eth1_to_eth2_fifo.readable)
        ]
        
        # ETH2 RX to ETH1 TX
        self.sync.eth2_rx += [
            If(self.eth2_rx_ctl,
               eth2_to_eth1_fifo.we.eq(1),
               eth2_to_eth1_fifo.din.eq(self.eth2_rx_data)
            ).Else(
               eth2_to_eth1_fifo.we.eq(0)
            )
        ]
        self.comb += [
            self.eth1_tx_data.eq(eth2_to_eth1_fifo.dout),
            self.eth1_tx_ctl.eq(~eth2_to_eth1_fifo.readable),
            eth2_to_eth1_fifo.re.eq(~eth2_to_eth1_fifo.readable)
        ]
        
        # Generate TX clocks (would need proper PLL in real design)
        counter1 = Signal(8)
        counter2 = Signal(8)
        self.sync += [
            counter1.eq(counter1 + 1),
            counter2.eq(counter2 + 1),
            self.eth1_tx_clk.eq(counter1[0]),
            self.eth2_tx_clk.eq(counter2[0])
        ]

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    
    # Generate Verilog
    top = EthernetBridge()
    verilog_output = verilog.convert(top, 
        ios={
            top.eth1_rx_clk, top.eth1_rx_ctl, top.eth1_rx_data,
            top.eth1_tx_clk, top.eth1_tx_ctl, top.eth1_tx_data,
            top.eth2_rx_clk, top.eth2_rx_ctl, top.eth2_rx_data,
            top.eth2_tx_clk, top.eth2_tx_ctl, top.eth2_tx_data
        }
    )
    
    # Write Verilog file
    with open("build/eth_bridge.v", "w") as f:
        f.write(verilog_output.main_source)
    
    print("Verilog file generated at: build/eth_bridge.v")
    print("To build the bitstream, use GoWin IDE to synthesize, P&R, and generate the bitstream")
    
    # Generate a sample constraint file
    constraint_file = """
// Pin constraints for Tang Nano 35K with YT8531C PHYs
IO_LOC "eth1_rx_clk" L2;
IO_LOC "eth1_rx_ctl" L1;
IO_LOC "eth1_rx_data[0]" K1;
IO_LOC "eth1_rx_data[1]" K2;
IO_LOC "eth1_rx_data[2]" B2;
IO_LOC "eth1_rx_data[3]" C2;
IO_LOC "eth1_tx_clk" F2;
IO_LOC "eth1_tx_ctl" F1;
IO_LOC "eth1_tx_data[0]" A1;
IO_LOC "eth1_tx_data[1]" D8;
IO_LOC "eth1_tx_data[2]" E1;
IO_LOC "eth1_tx_data[3]" D1;

IO_LOC "eth2_rx_clk" L6;
IO_LOC "eth2_rx_ctl" K6;
IO_LOC "eth2_rx_data[0]" G7;
IO_LOC "eth2_rx_data[1]" G8;
IO_LOC "eth2_rx_data[2]" F5;
IO_LOC "eth2_rx_data[3]" G5;
IO_LOC "eth2_tx_clk" H5;
IO_LOC "eth2_tx_ctl" J5;
IO_LOC "eth2_tx_data[0]" L5;
IO_LOC "eth2_tx_data[1]" K5;
IO_LOC "eth2_tx_data[2]" H8;
IO_LOC "eth2_tx_data[3]" H7;

IO_PORT "eth1_rx_clk" IO_TYPE=LVCMOS33;
IO_PORT "eth1_rx_ctl" IO_TYPE=LVCMOS33;
IO_PORT "eth1_rx_data[0]" IO_TYPE=LVCMOS33;
IO_PORT "eth1_rx_data[1]" IO_TYPE=LVCMOS33;
IO_PORT "eth1_rx_data[2]" IO_TYPE=LVCMOS33;
IO_PORT "eth1_rx_data[3]" IO_TYPE=LVCMOS33;
IO_PORT "eth1_tx_clk" IO_TYPE=LVCMOS33;
IO_PORT "eth1_tx_ctl" IO_TYPE=LVCMOS33;
IO_PORT "eth1_tx_data[0]" IO_TYPE=LVCMOS33;
IO_PORT "eth1_tx_data[1]" IO_TYPE=LVCMOS33;
IO_PORT "eth1_tx_data[2]" IO_TYPE=LVCMOS33;
IO_PORT "eth1_tx_data[3]" IO_TYPE=LVCMOS33;

IO_PORT "eth2_rx_clk" IO_TYPE=LVCMOS33;
IO_PORT "eth2_rx_ctl" IO_TYPE=LVCMOS33;
IO_PORT "eth2_rx_data[0]" IO_TYPE=LVCMOS33;
IO_PORT "eth2_rx_data[1]" IO_TYPE=LVCMOS33;
IO_PORT "eth2_rx_data[2]" IO_TYPE=LVCMOS33;
IO_PORT "eth2_rx_data[3]" IO_TYPE=LVCMOS33;
IO_PORT "eth2_tx_clk" IO_TYPE=LVCMOS33;
IO_PORT "eth2_tx_ctl" IO_TYPE=LVCMOS33;
IO_PORT "eth2_tx_data[0]" IO_TYPE=LVCMOS33;
IO_PORT "eth2_tx_data[1]" IO_TYPE=LVCMOS33;
IO_PORT "eth2_tx_data[2]" IO_TYPE=LVCMOS33;
IO_PORT "eth2_tx_data[3]" IO_TYPE=LVCMOS33;
"""
    
    with open("build/eth_bridge.cst", "w") as f:
        f.write(constraint_file)
    
    print("Constraint file generated at: build/eth_bridge.cst") 