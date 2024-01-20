def set_bit(target, bit):
    """
    Set a specific bit to 1 in the target number.

    Args:
        target (int): The number in which the bit is to be set.
        bit (int): The position of the bit to be set (0-indexed).

    Returns:
        int: The modified number with the specified bit set to 1.
    """
    return target | (1 << bit)

def clear_bit(target, bit):
    """
    Set a specific bit to 0 in the target number.

    Args:
        target (int): The number in which the bit is to be cleared.
        bit (int): The position of the bit to be cleared (0-indexed).

    Returns:
        int: The modified number with the specified bit set to 0.
    """
    return target & ~(1 << bit)

def is_bit_high(value, bit):
    """
    Check if a specific bit is set to 1 in a number.

    Args:
        value (int): The number to check.
        bit (int): The position of the bit to check (0-indexed).

    Returns:
        bool: True if the specified bit is 1, False otherwise.
    """
    return (value & (1 << bit)) != 0

def is_bit_low(value, bit):
    """
    Check if a specific bit is set to 0 in a number.

    Args:
        value (int): The number to check.
        bit (int): The position of the bit to check (0-indexed).

    Returns:
        bool: True if the specified bit is 0, False otherwise.
    """
    return (value & (1 << bit)) == 0

def get_lower_nibble(value):
    """
    Get the lower nibble (4 bits) from a byte.

    Args:
        value (int): The byte from which the lower nibble is extracted.

    Returns:
        int: The lower nibble of the given byte.
    """
    return value & 0x0F

def get_upper_nibble(value):
    """
    Get the upper nibble (4 bits) from a byte.

    Args:
        value (int): The byte from which the upper nibble is extracted.

    Returns:
        int: The upper nibble of the given byte.
    """
    return (value & 0xF0) >> 4

def set_high_byte(target, hi_byte):
    """
    Set the high byte of a 16-bit (or longer) number.

    Args:
        target (int): The original number.
        hi_byte (int): The byte to set as the high byte.

    Returns:
        int: The modified number with the high byte replaced.
    """
    return (target & 0x00FF) | (hi_byte << 8)

def set_low_byte(target, lo_byte):
    """
    Set the low byte of a 16-bit (or longer) number.

    Args:
        target (int): The original number.
        lo_byte (int): The byte to set as the low byte.

    Returns:
        int: The modified number with the low byte replaced.
    """
    return (target & 0xFF00) | lo_byte
