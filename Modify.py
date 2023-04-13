from pathlib import Path
from strongarm.macho import MachoParser, MachoBinary, MachoAnalyzer
from strongarm.macho.macho_binary_writer import MachoBinaryWriter

# Load an input file
macho_parser = MachoParser(Path() / "TestApp")
# Read the ARM64 slice and perform some operations
binary: MachoBinary = macho_parser.get_arm64_slice()

# Read cstring segment information
cstring = binary.section_with_name("__cstring", "__TEXT")
pointer: int = cstring.address
size: int = cstring.size + pointer

# Parse cstrings
while pointer < size:
  str = binary.read_string_at_address(pointer)
  if str == None:
    pointer += 1
    continue
  if str == "Select a Landmark":
    print("Found the string.")
    break
  pointer += str.__len__() + 1

# Overwrite the text
modified_binary = binary.write_bytes(bytes.fromhex('48656c6c6f20277374726f6e6761726d27'), pointer, True)
# Persist the modified binary to disk
modified_binary.write_binary(Path() / "ModifiedTestApp")
# Validate modification
print(modified_binary.read_string_at_address(pointer))
# Prints Hello 'strongarm'