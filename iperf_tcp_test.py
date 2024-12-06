import pytest
from parser import parse_iperf_output

class TestSuite:
    def test_iperf3_client_connection(self, client):
        output, error = client
        assert not error, f"Client error: {error}"

        stats = parse_iperf_output(output)
        assert stats, "No valid stats parsed from iperf client output."

        # Validate Transfer and Bitrate conditions
        for stat in stats:
            transfer_value, transfer_unit = re.match(r"([\d.]+)\s+(\w+)", stat["Transfer"]).groups()
            bitrate_value, bitrate_unit = re.match(r"([\d.]+)\s+(\w+/sec)", stat["Bitrate"]).groups()

            transfer_value = float(transfer_value)
            bitrate_value = float(bitrate_value)

            if transfer_unit == "MBytes":
                transfer_value /= 1024
            if bitrate_unit == "Mbits/sec":
                bitrate_value /= 1000

            assert transfer_value > 2, f"Transfer {transfer_value} GB is below the threshold."
            assert bitrate_value > 20, f"Bitrate {bitrate_value} Gbits/sec is below the threshold."
