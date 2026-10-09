import asyncio
import time

import aiohttp
import requests

URLS = [
    "https://www.google.com",
    "https://www.python.org",
    "https://httpbin.org/delay/2",
    "https://www.github.com",
]

TIMEOUT = 15


def fetch_sync(url: str):
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=TIMEOUT)
        status = response.status_code
    except Exception as exc:
        status = f"ERROR: {exc}"
    return url, status, time.perf_counter() - start


def fetch_all_sync(urls):
    start = time.perf_counter()
    results = [fetch_sync(url) for url in urls]
    return results, time.perf_counter() - start


async def fetch_url(session, url: str):
    start = time.perf_counter()
    try:
        timeout = aiohttp.ClientTimeout(total=TIMEOUT)
        async with session.get(url, timeout=timeout) as response:
            status = response.status
    except Exception as exc:
        status = f"ERROR: {exc}"
    return url, status, time.perf_counter() - start


async def fetch_all_async(urls, session_factory=aiohttp.ClientSession):
    start = time.perf_counter()
    async with session_factory() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return list(results), time.perf_counter() - start


def _print_results(title, results, total):
    print(f"\n=== {title} ===")
    for url, status, elapsed in results:
        print(f"  {url:40s} status={status} time={elapsed:.3f}s")
    print(f"  Total: {total:.3f}s")


def main():
    sync_results, sync_total = fetch_all_sync(URLS)
    _print_results("SYNC", sync_results, sync_total)

    async_results, async_total = asyncio.run(fetch_all_async(URLS))
    _print_results("ASYNC", async_results, async_total)

    print(f"\nУскорение: {sync_total / async_total:.2f}x")


if __name__ == "__main__":
    main()