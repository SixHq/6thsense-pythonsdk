___bccc___ = 4
___bccd___ = 24
___bcce___ = 25


def bytes_to_string(byte_data, encoding='utf-8', errors='strict'):
    try:
        string_data = byte_data.decode(encoding, errors)
        return string_data
    except UnicodeDecodeError as e:
        print(f"Error decoding byte data: {e}")
        return None