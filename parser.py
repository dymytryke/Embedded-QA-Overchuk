import re

def parse_iperf_output(output):
    stats = []
    lines = output.split("\n")
    for line in lines:
        match = re.search(r"(\d+\.\d+-\d+\.\d+)\s+sec\s+([\d.]+\s+\w+)\s+([\d.]+\s+\w+/sec)", line)
        if match:
            stats.append({
                "Interval": match.group(1),
                "Transfer": match.group(2),
                "Bitrate": match.group(3),
            })
    return stats
