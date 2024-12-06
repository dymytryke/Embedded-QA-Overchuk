import re;

def filter_stats(stats):
    filtered_stats = []
    for stat in stats:
        # Extract numeric values from Transfer and Bitrate
        transfer_value, transfer_unit = re.match(r"([\d.]+)\s+(\w+)", stat["Transfer"]).groups()
        bitrate_value, bitrate_unit = re.match(r"([\d.]+)\s+(\w+/sec)", stat["Bitrate"]).groups()

        transfer_value = float(transfer_value)
        bitrate_value = float(bitrate_value)

        # Convert units to GB and Gbits/sec for comparison
        if transfer_unit == "MBytes":
            transfer_value /= 1024
        if bitrate_unit == "Mbits/sec":
            bitrate_value /= 1000

        # Check conditions: Transfer > 2 GB and Bitrate > 20 Gbits/sec
        if transfer_value > 2 and bitrate_value > 20:
            filtered_stats.append(stat)

    return filtered_stats
