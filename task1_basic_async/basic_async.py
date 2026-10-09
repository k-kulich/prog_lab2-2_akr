import asyncio
import time


async def delayed_print(message: str, delay: float) -> str:
    """Ждёт `delay` секунд и выводит `message`."""
    await asyncio.sleep(delay)
    print(message)
    return message


async def main():
    start = time.perf_counter()
    await delayed_print("Hello after 1 second", 1)
    print(f"Elapsed: {time.perf_counter() - start:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())