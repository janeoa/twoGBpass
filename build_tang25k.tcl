set proj_name       "bitstream"
#set device_part    "GW5A-LV25MG121N"
set device_part     "GW5A-LV25MG121NC1/I0"
#set device_version "NA"
set device_version  "A"
set proj_dir        "/workspace"

create_project \
  -name ${proj_name} \
  -dir  ${proj_dir} \
  -pn   ${device_part} \
  -device_version ${device_version} \
  -force

add_file   -type verilog /workspace/build/eth_bridge.v
add_file   -type cst     /workspace/build/eth_bridge.cst
set_option -top_module  top
#run        syn
#run        pnr
run        all       ;# or program_device, depending on your version
#project_close
exit
