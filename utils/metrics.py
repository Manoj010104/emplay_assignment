# utils/metrics.py

import time

class MetricsTracker:
    def __init__(self):
        self.latency = 0.0
        self.token_usage = 0
        self.query_count = 0

    def start_timer(self):
        self.start_time = time.perf_counter()

    def stop_timer(self):
        if hasattr(self, 'start_time'):
            self.latency += (time.perf_counter() - self.start_time)
            del self.start_time

    def add_token_usage(self, tokens: int):
        self.token_usage += tokens

    def increment_query_count(self):
        self.query_count += 1

    def get_average_latency(self):
        if self.query_count == 0:
            return 0
        return self.latency / self.query_count

    def get_total_token_usage(self):
        return self.token_usage

    def reset(self):
        self.latency = 0.0
        self.token_usage = 0
        self.query_count = 0

    def __str__(self):
        return (
            f"Metrics Summary:\n"
            f"  Queries Processed: {self.query_count}\n"
            f"  Average Latency: {self.get_average_latency():.2f} seconds\n"
            f"  Total Token Usage: {self.get_total_token_usage()} tokens"
        )