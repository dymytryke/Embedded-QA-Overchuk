import pytest
from parser import parse_iperf_output
from filter import filter_stats

class TestSuite:
    def test_iperf3_client_connection(self, client):
        """
        Verifies that iperf client returns valid data and filters statistics
        meeting thresholds.
        """
        output, error = client
        assert not error, f"Client error: {error}"

        # Parse the iperf output
        stats = parse_iperf_output(output)
        assert stats, "No valid stats parsed from iperf client output."

        # Filter the stats
        filtered_stats = filter_stats(stats)

        # Ensure there are stats meeting the threshold
        assert filtered_stats, "No intervals meet the filtering criteria."

        # Optionally, print filtered stats for debugging purposes
        for stat in filtered_stats:
            print(stat)
