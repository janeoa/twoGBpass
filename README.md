This project aim to make a FPGA bitstream for the tang25k SoM on the custom board to make a ethernet to ethernet passthough channel.

# Usage
## Build the container
```bash
docker build . -t gowin-docker:latest
```
## Run the container
```bash
docker run --rm -it \
    --mac-address <your-mac-address> \
    -v <path-to-gowin-license>:/data/license.lic \
    -v <path-to-project-directory>:/workspace \
    gowin-docker:latest <python-top-module-file> <tcl-file>

# example 
# docker run --rm -it \
#    --mac-address 00:11:22:33:44:55 \
#    -v ~/dev/gowin-docker/gowin_E_....lic:/data/license.lic \
#    -v ~/dev/twogigabits:/workspace \
#    gowin-docker:latest eth_bridge.py build_tang25k.tcl
```


# SoM
FPGA GW5A-LV25MG121C1/l0

# Board
two RJ45 ports with Motorcom YT8531C PHY IC each.

# Library
Heavily relies on oss-cad-suite and litex, that are wrapped in the docker

This project uses https://github.com/enjoy-digital/liteeth

# Pinout
|Bank |GPIO           |connector|connector pin|connected to|
|-----|---------------|---------|-------------|------------|
|BANK1|H5_IOT61A      |J1       |P4           |E2 TX CLK   |
|BANK1|J5_IOT61B      |J1       |P6           |E2 TX CTL   |
|BANK1|L5_IOT63A      |J1       |P8           |E2 TX D0    |
|BANK1|K5_IOT63B      |J1       |P10          |E2 TX D1    |
|BANK1|H8_IOT66A      |J1       |P12          |E2 TX D2    |
|BANK1|H7_IOT66B      |J1       |P14          |E2 TX D3    |
|BANK1|G7_IOT68A      |J1       |P16          |E2 RX D0    |
|BANK1|G8_IOT68B      |J1       |P18          |E2 RX D1    |
|BANK1|F5_IOT72A      |J1       |P20          |E2 RX D2    |
|BANK1|G5_IOT72B      |J1       |P22          |E2 RX D3    |
|BANK5|B2_IOB4A_40P   |J2       |P3           |E1 RX D2    |
|BANK5|C2_IOB4B_40P   |J2       |P5           |E1 RX D3    |
|BANK5|F2_IOB26A_40P  |J2       |P7           |E1 TX CLK   |
|BANK5|F1_IOB26B_40P  |J2       |P9           |E1 TX CTL   |
|BANK5|A1_IOB24A_40P  |J2       |P11          |E1 TX D0    |
|BANK5|D8_RECONFIG    |J2       |P13          |E1 TX D1    |
|BANK5|E1_IOB12B_40P  |J2       |P15          |E1 TX D2    |
|BANK5|D1_IOB14B_40P  |J2       |P17          |E1 TX D3    |
|BANK2|L2_IOR18A_40P  |J2       |P6           |E1 RX CLK   |
|BANK2|L1_IOR18B_40P  |J2       |P8           |E1 RX CTL   |
|BANK2|K1_IOR20A_40P  |J2       |P10          |E1 RX D0    |
|BANK2|K2_IOR20B_40P  |J2       |P12          |E1 RX D1    |
|BANK7|L6_IOT23A_USB_P|J1       |P30          |E2 RX CLK   |
|BANK7|K6_IOT23B_USB_N|J1       |P32          |E2 RX CTL   |
|BANK7|K7_IOT21A_40P  |J1       |P34          |MDIO        |
|BANK7|J7_IOT21B_40P  |J1       |P36          |MDC         |
