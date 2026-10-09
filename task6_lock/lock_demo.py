import threading
import time

counter = 0
lock = threading.Lock()


def safe_increment(iterations: int = 1000, work_delay: float = 0.0001) -> None:
    """Безопасное увеличение глобального счетчика."""
    global counter
    for _ in range(iterations):
        with lock:
            temp = counter
            time.sleep(work_delay)
            counter = temp + 1


def run_safe(threads_count: int = 5, iterations: int = 1000) -> int:
    global counter
    counter = 0
    threads = [
        threading.Thread(target=safe_increment, args=(iterations,))
        for _ in range(threads_count)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter


def main():
    expected = 5 * 1000
    result = run_safe()
    print(f"Expected: {expected}")
    print(f"Actual:   {result}")
    print("OK" if result == expected else "FAIL")


if __name__ == "__main__":
    main()