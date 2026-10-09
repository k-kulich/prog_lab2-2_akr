import asyncio
import os
import sys
import time

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "task1_basic_async"),
)

from basic_async import delayed_print


async def run_all():
    start = time.perf_counter()
    await asyncio.gather(
        delayed_print("Message A (delay=2)", 2),
        delayed_print("Message B (delay=1)", 1),
        delayed_print("Message C (delay=3)", 3),
    )
    return time.perf_counter() - start


async def main():
    elapsed = await run_all()
    print(f"Total elapsed: {elapsed:.3f}s (ожидается ~3с, а не 6с)")


if __name__ == "__main__":
    asyncio.run(main())