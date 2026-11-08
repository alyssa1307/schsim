import csv
class Process:
    def __init__(self, name, arrival, service):
        self.name = name
        self.arrival = arrival
        self.service = service
        self.remaining = service
        self.start = None
        self.finish = None
        self.waiting = 0



def read_processes(filename):
    processes = []

    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row or row[0].strip() == "":
                continue

            name = row[0].strip()
            arrival = int(row[1])
            service = int(row[2])

            process = Process(name, arrival, service)
            processes.append(process)

    return processes


# Test reading the input file
processes = read_processes("examples/input1/in.csv")

for process in processes:
    print(process.name, process.arrival, process.service)


def first_come_first_served(processes):
    current_time = 0

    # Process jobs in arrival order
    processes.sort(key=lambda p: p.arrival)

    for process in processes:
        # Wait until the process arrives
        if current_time < process.arrival:
            current_time = process.arrival

        # Start running the process
        process.start = current_time

        # Run the process until it finishes
        current_time += process.service
        process.remaining = 0

        # Record scheduling statistics
        process.finish = current_time
        process.waiting = process.start - process.arrival

    return processes


print("\nFirst-Come-First-Served Results:")

results = first_come_first_served(processes)

for process in results:
    turnaround = process.finish - process.arrival
    normalized = turnaround / process.service

    print(
        process.name,
        "Start:", process.start,
        "Finish:", process.finish,
        "Turnaround:", turnaround,
        "Normalized:", f"{normalized:.2f}"
    )


def shortest_process_next(processes):
    current_time = 0
    completed = []
    ready = processes.copy()

    while ready:
        # Find processes that have arrived
        available = [
            p for p in ready
            if p.arrival <= current_time
        ]

        # If none have arrived, advance the clock
        if not available:
            current_time = min(p.arrival for p in ready)
            continue

        # Select the process with the shortest service time
        process = min(available, key=lambda p: p.service)

        process.start = current_time
        current_time += process.service
        process.remaining = 0
        process.finish = current_time
        process.waiting = process.start - process.arrival

        completed.append(process)
        ready.remove(process)

    return completed


# Read fresh processes so FF results are not overwritten
sp_processes = read_processes("examples/input1/in.csv")
sp_results = shortest_process_next(sp_processes)

print("\nShortest Process Next Results:")

for process in sp_results:
    turnaround = process.finish - process.arrival
    normalized = turnaround / process.service

    print(
        process.name,
        "Start:", process.start,
        "Finish:", process.finish,
        "Turnaround:", turnaround,
        "Normalized:", f"{normalized:.2f}"
    )


from collections import deque


def round_robin(processes, quantum=2):
    current_time = 0
    completed = []
    ready = deque()

    # Sort processes by arrival time
    arrivals = sorted(processes, key=lambda p: p.arrival)
    next_arrival = 0

    while len(completed) < len(processes):

        # Move newly arrived processes into Ready Queue
        while (next_arrival < len(arrivals)
               and arrivals[next_arrival].arrival <= current_time):
            ready.append(arrivals[next_arrival])
            next_arrival += 1

        if not ready:
            current_time += 1
            continue

        # Select the first process in the Ready Queue
        process = ready.popleft()

        if process.start is None:
            process.start = current_time

        # Run for the quantum or until the process finishes
        run_time = min(quantum, process.remaining)
        current_time += run_time
        process.remaining -= run_time

        # Add any processes that arrived while CPU was running
        while (next_arrival < len(arrivals)
               and arrivals[next_arrival].arrival <= current_time):
            ready.append(arrivals[next_arrival])
            next_arrival += 1

        if process.remaining == 0:
            process.finish = current_time
            process.waiting = (
                process.finish - process.arrival - process.service
            )
            completed.append(process)
        else:
            ready.append(process)

    return completed


rr_processes = read_processes("examples/input1/in.csv")
rr_results = round_robin(rr_processes, quantum=2)

print("\nRound Robin Results (Quantum = 2):")

for process in rr_results:
    turnaround = process.finish - process.arrival
    normalized = turnaround / process.service

    print(
        process.name,
        "Start:", process.start,
        "Finish:", process.finish,
        "Turnaround:", turnaround,
        "Normalized:", f"{normalized:.2f}"
    )


def shortest_remaining_time(processes):
    current_time = 0
    completed = []

    while len(completed) < len(processes):

        # Find processes that have arrived and are not finished
        ready = [
            p for p in processes
            if p.arrival <= current_time and p.remaining > 0
        ]

        # If no process is ready, advance the clock
        if not ready:
            current_time += 1
            continue

        # Select the process with the shortest remaining time
        process = min(ready, key=lambda p: p.remaining)

        # Record the first time the process uses the CPU
        if process.start is None:
            process.start = current_time

        # Run the selected process for one CPU cycle
        process.remaining -= 1
        current_time += 1

        # Check whether the process has finished
        if process.remaining == 0:
            process.finish = current_time
            process.waiting = (
                process.finish - process.arrival - process.service
            )
            completed.append(process)

    return completed



def first_come_first_served(processes):
    current_time = 0

    # Sort processes by when they arrive
    processes.sort(key=lambda p: p.arrival)

    for process in processes:
        # Move the clock forward if the CPU is waiting
        if current_time < process.arrival:
            current_time = process.arrival

        # Record when the process starts running
        process.start = current_time

        # Run the process until it finishes
        current_time += process.service
        process.remaining = 0

        # Save the finish time and waiting time
        process.finish = current_time
        process.waiting = process.start - process.arrival

    return processes
