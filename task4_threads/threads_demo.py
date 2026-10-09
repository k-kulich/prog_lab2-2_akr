import threading
import time


def print_message(message: str, delay: float) -> None:
    time.sleep(delay)
    print(message)


def run_sequential(tasks) -> float:
    start = time.perf_counter()
    for message, delay in tasks:
        print_message(message, delay)
    return time.perf_counter() - start


def run_threaded(tasks) -> float:
    start = time.perf_counter()
    threads = [
        threading.Thread(target=print_message, args=(message, delay))
        for message, delay in tasks
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


TASKS = [
    ("Message 1", 2.0),
    ("Message 2", 2.0),
    ("Message 3", 2.0),
]


def main():
    print("=== Sequential ===")
    seq_time = run_sequential(TASKS)
    print(f"Sequential total: {seq_time:.3f}s")

    print("\n=== Threaded ===")
    thr_time = run_threaded(TASKS)
    print(f"Threaded total: {thr_time:.3f}s")

    print(f"\nУскорение: {seq_time / thr_time:.2f}x")


if __name__ == "__main__":
    main()