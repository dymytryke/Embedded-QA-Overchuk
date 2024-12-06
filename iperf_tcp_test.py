import subprocess
import re
import argparse

def run_iperf_client(server_ip, interval):
    try:
        # Build the iperf command
        command = ["iperf", "-c", server_ip, "-i", str(interval)]

        # Execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        return output.decode(), error.decode()

    except Exception as e:
        return "", str(e)


def parse_iperf_output(output):
    stats = []
    lines = output.split("\n")
    for line in lines:
        # Match lines containing interval, transfer, and bitrate
        match = re.search(r"(\d+\.\d+-\d+\.\d+)\s+sec\s+([\d.]+\s+\w+)\s+([\d.]+\s+\w+/sec)", line)
        if match:
            stats.append({
                "Interval": match.group(1),
                "Transfer": match.group(2),
                "Bitrate": match.group(3),
            })
    return stats


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


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Automated iPerf TCP Test")
    parser.add_argument("server_ip", type=str, help="IP address of the iPerf server")
    parser.add_argument("interval", type=int, help="Reporting interval in seconds")
    args = parser.parse_args()

    server_ip = args.server_ip
    interval = args.interval

    print(f"Running TCP test with server IP: {server_ip} and interval: {interval} seconds...\n")
    
    # Run the iPerf client
    tcp_output, tcp_error = run_iperf_client(server_ip, interval)
    if tcp_error:
        print("Error during test:", tcp_error)
    else:
        tcp_stats = parse_iperf_output(tcp_output)
        if tcp_stats:
            filtered_stats = filter_stats(tcp_stats)
            if filtered_stats:
                print("Filtered TCP Test Results (Transfer > 2 GB and Bitrate > 20 Gbits/sec):")
                for stat in filtered_stats:
                    print(stat)
            else:
                print("No intervals meet the filtering criteria.")
        else:
            print("No statistics parsed. Please check the server or client output.")


if __name__ == "__main__":
    main()
