#!/bin/bash

# Check if the required arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: run_build.sh <python_file> <tcl_file>"
    exit 1
fi

PYTHON_FILE=$1
TCL_FILE=$2

# Ensure the workspace directory exists
if [ ! -d "/workspace" ]; then
    echo "Error: /workspace directory not found!"
    exit 1
fi

# Run the Python file
echo "Running Python file: $PYTHON_FILE"
source /usr/local/share/litex/venv/bin/activate
python3 "/workspace/$PYTHON_FILE"

# Run the Gowin toolchain with the .tcl file
echo "Running Gowin toolchain with TCL file: $TCL_FILE"
gw_sh "/workspace/$TCL_FILE"

