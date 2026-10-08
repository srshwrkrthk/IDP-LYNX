import statistics
import time
from collections import deque
from threading import Lock

from pynput import keyboard


class HIDMonitor:
    def __init__(self):
        self.timestamps = deque()
        self.lock = Lock()
        self.listener = keyboard.Listener(on_press=self._on_press)

    def _on_press(self, _key):
        now = time.monotonic()

        with self.lock:
            self.timestamps.append(now)

            cutoff = now - 120

            while self.timestamps and self.timestamps[0] < cutoff:
                self.timestamps.popleft()

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def summarize(
        self,
        device_id: str,
        started_at: float,
        ended_at: float,
    ) -> dict:
        with self.lock:
            timestamps = [
                value
                for value in self.timestamps
                if started_at <= value <= ended_at
            ]

        intervals = [
            (timestamps[index] - timestamps[index - 1]) * 1000
            for index in range(1, len(timestamps))
        ]

        average_interval = (
            statistics.fmean(intervals)
            if intervals
            else None
        )

        interval_stddev = (
            statistics.pstdev(intervals)
            if len(intervals) >= 2
            else None
        )

        first_key_delay = (
            int((timestamps[0] - started_at) * 1000)
            if timestamps
            else None
        )

        return {
            "device_id": device_id,
            "observation_window_ms": int(
                (ended_at - started_at) * 1000
            ),
            "key_count": len(timestamps),
            "first_key_delay_ms": first_key_delay,
            "average_interval_ms": average_interval,
            "interval_stddev_ms": interval_stddev,
            "max_keys_per_second": self._maximum_rate(timestamps),
        }

    @staticmethod
    def _maximum_rate(timestamps: list[float]) -> float:
        maximum = 0
        left = 0

        for right, timestamp in enumerate(timestamps):
            while timestamp - timestamps[left] > 1:
                left += 1

            maximum = max(maximum, right - left + 1)

        return float(maximum)