# Imports PSP Linker .map file symbols with 0x08804000 rebase
# @category PSP

import os

BASE_ADDRESS = 0x08804000

map_file = askFile("Select .map file", "Open")
listing = currentProgram.getListing()
symbol_table = currentProgram.getSymbolTable()

success = 0

with open(map_file.getAbsolutePath(), "r") as f:
    for line in f:
        parts = line.split()
        # Look for lines with valid 8-digit hex addresses:
        # e.g., "00010200 00000040 ... FunctionName"
        if len(parts) >= 2 and len(parts[0]) == 8:
            try:
                rel_addr = int(parts[0], 16)
                symbol_name = parts[-1]
                
                # Filter out section headers and defaults
                if symbol_name.startswith(('.', '<', '*')) or symbol_name == "Symbol":
                    continue
                
                # Apply base address offset
                target_addr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(rel_addr + BASE_ADDRESS)
                
                # Create label in Ghidra
                createLabel(target_addr, symbol_name, True)
                success += 1
            except ValueError:
                continue

print("Successfully imported {} symbols!".format(success))