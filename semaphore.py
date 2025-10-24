import threading

buffer = []
in_index = 0
out_index = 0
item = 0
size = 0

empty = None
full = None
mutex = threading.Lock()

def produce():
    global buffer, in_index, item
    if empty.acquire(blocking=False):
        with mutex:
            item += 1
            buffer[in_index] = item
            print(f"Produced item {item}")
            in_index = (in_index + 1) % size
        full.release()
    else:
        print("Buffer full!")

def consume():
    global buffer, out_index
    if full.acquire(blocking=False):
        with mutex:
            consumed = buffer[out_index]
            print(f"Consumed item {consumed}")
            out_index = (out_index + 1) % size
        empty.release()
    else:
        print("Buffer empty!")

def main():
    global buffer, size, empty, full
    size = int(input("Enter buffer size: "))
    buffer = [0] * size
    empty = threading.Semaphore(size)
    full = threading.Semaphore(0)

    while True:
        print("\n1. Produce\n2. Consume\n3. Exit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            produce()
        elif choice == 2:
            consume()
        elif choice == 3:
            break

if __name__ == "__main__":
    main()
