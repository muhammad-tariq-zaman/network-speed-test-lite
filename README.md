# network-speed-test-lite

Measure real download latency and throughput for a given URL with `urllib`.
It reports only measured values — byte count, elapsed time, KB/s, and
time-to-first-byte. On failure it reports the error, never an invented speed.

## How to run

```bash
python3 main.py https://example.com/sample.bin
```

## Example output (sample from test fixture data)

```text
OK  https://example.test/file.bin: 10000 bytes in 0.01 s (976.5 KB/s, TTFB 0.1 ms)
```

Tests mock `urllib`, so they run without network access. (Actual KB/s in a
real run depends on the live connection; the figure above is from the mock.)
