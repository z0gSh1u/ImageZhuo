# Utilities
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo


# Convert bytes data to integer.
def bytesToInt(bytes_, littleEndian=True):
    return int.from_bytes(bytes_, 'little' if littleEndian else 'big')


# Convert interger to bytes data.
def intToBytes(int_, byteLength: int, littleEndian=True):
    return int.to_bytes(int(int_), byteLength,
                        'little' if littleEndian else 'big')


# Forbid QT Component resize.
def disableResize(qtComponent):
    qtComponent.setFixedSize(qtComponent.size())
