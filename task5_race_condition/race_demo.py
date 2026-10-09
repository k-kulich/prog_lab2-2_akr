import threading
import time

counter = 0


def unsafe_increment(iterations: int = 1000, work_delay: float = 0.0001) -> None:
    """Специально небезопасное увеличение глобального счетчика.
    Между чтением и записью есть небольшая пауза, которая увеличивает
    окно гонки и делает потерю данных хорошо заметной.
    """
    global counter
    for _ in range(iterations):
        temp = counter
        time.sleep(work_delay)
        counter = temp + 1


def run_race(threads_count: int = 5, iterations: int = 1000) -> int:
    global counter
    counter = 0
    threads = [
        threading.Thread(target=unsafe_increment, args=(iterations,))
        for _ in range(threads_count)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter


def main():
    expected = 5 * 1000
    result = run_race()
    print(f"Expected: {expected}")
    print(f"Actual:   {result}")
    print(f"Lost:     {expected - result}")


if __name__ == "__main__":
    main()