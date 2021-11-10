# Utilities
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

# Convert bytes data to integer.
def bytesToInt(bytes, littleEndian=True):
  return int.from_bytes(bytes, 'little' if littleEndian else 'big')

def disableResize(qtComponent):
  qtComponent.setFixedSize(qtComponent.size())