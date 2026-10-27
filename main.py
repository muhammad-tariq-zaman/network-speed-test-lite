"""Network speed test lite: measure real download latency/throughput via urllib."""
import argparse
import sys
import time
import urllib.request


def measure(url, timeout=15, chunk=65536):
    start = time.monotonic()
    total = 0
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            first_byte_at = None
            while True:
                data = resp.read(chunk)
                if not data:
                    break
                if first_byte_at is None:
                    first_byte_at = time.monotonic()
                total += len(data)
    except Exception as exc:
        return {"url": url, "status": "ERROR", "error": str(exc),
                "bytes": 0, "seconds": None, "kb_per_sec": None, "ttfb_ms": None}
    elapsed = time.monotonic() - start
    ttfb = None if first_byte_at is None else round((first_byte_at - start) * 1000, 1)
    return {"url": url, "status": "OK", "error": "",
            "bytes": total, "seconds": round(elapsed, 2),
            "kb_per_sec": round(total / 1024 / elapsed, 1) if elapsed > 0 else 0,
            "ttfb_ms": ttfb}


def main(argv=None):
    p = argparse.ArgumentParser(description="Measure real download speed for a URL.")
    p.add_argument("url")
    p.add_argument("--timeout", type=int, default=15)
    args = p.parse_args(argv)
    r = measure(args.url, args.timeout)
    if r["status"] == "ERROR":
        print(f"ERROR  {r['url']}: {r['error']}")
    else:
        print(f"OK  {r['url']}: {r['bytes']} bytes in {r['seconds']} s "
              f"({r['kb_per_sec']} KB/s, TTFB {r['ttfb_ms']} ms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
