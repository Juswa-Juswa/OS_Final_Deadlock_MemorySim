import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# =========================
# Banker's Algorithm Class
# =========================
class BankersAlgorithm:
    # Constructor to initialize the Banker's Algorithm
    def __init__(self, processes, max_resources, available_resources):
        self.processes = processes  # Number of processes
        self.max_resources = max_resources  # Maximum resources each process can request
        self.available_resources = available_resources  # Available resources in the system
        self.allocation = [[0] * len(max_resources) for _ in range(processes)]  # Current allocation for each process
        self.max_need = [[max_resources[i] // 2 for i in range(len(max_resources))] for _ in range(processes)]  # Max need per process
        self.need = [[self.max_need[i][j] - self.allocation[i][j] for j in range(len(max_resources))] for i in range(processes)]  # Current need

    # Request resources for a given process
    def request_resources(self, process_id, request):
        # Check if the request is valid (does not exceed the need and available resources)
        if all(request[i] <= self.need[process_id][i] for i in range(len(request))) and \
           all(request[i] <= self.available_resources[i] for i in range(len(request))):
            # Allocate resources for the given process
            for i in range(len(request)):
                self.available_resources[i] -= request[i]
                self.allocation[process_id][i] += request[i]
                self.need[process_id][i] -= request[i]
            # Check if the system is in a safe state after allocation
            if self.is_safe():
                return True
            else:
                # If not safe, undo the allocation (rollback)
                for i in range(len(request)):
                    self.available_resources[i] += request[i]
                    self.allocation[process_id][i] -= request[i]
                    self.need[process_id][i] += request[i]
                return False
        # If the request is invalid, return False
        return False

    # Check if the system is in a safe state
    def is_safe(self):
        work = self.available_resources[:]  # Copy of available resources
        finish = [False] * self.processes  # Track finished processes
        safe_sequence = []  # Track safe sequence

        # Loop until all processes are finished
        while len(safe_sequence) < self.processes:
            found = False
            for p in range(self.processes):
                # Check if process can be satisfied with current work
                if not finish[p] and all(self.need[p][i] <= work[i] for i in range(len(work))):
                    for i in range(len(work)):
                        work[i] += self.allocation[p][i]  # Simulate resource allocation
                    finish[p] = True
                    safe_sequence.append(p)
                    found = True
                    break
            if not found:
                return False  # Not safe
        return True  # Safe

# =========================
# Memory Allocator Class
# =========================
class MemoryAllocator:
    # Class to manage memory allocation using different algorithms
    def __init__(self, memory_blocks):
        self.memory_blocks = memory_blocks  # Store the available memory blocks

    def first_fit(self, process_size):
        # Allocate memory using the first fit algorithm
        for i in range(len(self.memory_blocks)):
            if self.memory_blocks[i] >= process_size:
                self.memory_blocks[i] -= process_size  # Allocate block
                return True
        return False  # No block large enough

    def best_fit(self, process_size):
        # Allocate memory using the best fit algorithm
        best_index = -1
        for i in range(len(self.memory_blocks)):
            if self.memory_blocks[i] >= process_size:
                if best_index == -1 or self.memory_blocks[best_index] > self.memory_blocks[i]:
                    best_index = i
        if best_index != -1:
            self.memory_blocks[best_index] -= process_size
            return True
        return False

    def worst_fit(self, process_size):
        # Allocate memory using the worst fit algorithm
        worst_index = -1
        for i in range(len(self.memory_blocks)):
            if self.memory_blocks[i] >= process_size:
                if worst_index == -1 or self.memory_blocks[worst_index] < self.memory_blocks[i]:
                    worst_index = i
        if worst_index != -1:
            self.memory_blocks[worst_index] -= process_size
            return True
        return False

# =========================
# Simulation Function
# =========================
def simulate_memory_allocation_and_deadlock(scenario):
    processes = len(scenario)  # Number of processes = number of requests
    max_resources = [10, 5, 7]  # System-wide resource limits
    available_resources = [3, 2, 2]  # Initial available resources
    banker = BankersAlgorithm(processes, max_resources, available_resources)  # Banker's Algorithm instance

    memory_blocks = [100, 500, 200, 300, 600]  # Initial memory blocks
    allocator = MemoryAllocator(memory_blocks)  # Memory allocator instance

    # Results dictionaries for each strategy
    allocation_results = {'First Fit': [], 'Best Fit': [], 'Worst Fit': []}
    fragmentation_results = {'First Fit': [], 'Best Fit': [], 'Worst Fit': []}
    runtime_results = {'First Fit': [], 'Best Fit': [], 'Worst Fit': []}
    deadlock_results = {'First Fit': [], 'Best Fit': [], 'Worst Fit': []}

    # Simulate each process/request in the scenario
    for process_id, (request, process_size) in enumerate(scenario):
        allocation_success = banker.request_resources(process_id, request)  # Try to allocate resources

        # First Fit
        start_time = time.time()
        first_fit_success = allocator.first_fit(process_size)
        end_time = time.time()
        runtime_results['First Fit'].append(end_time - start_time)  # Store runtime
        allocation_results['First Fit'].append(first_fit_success)  # Store allocation result
        deadlock_results['First Fit'].append(not allocation_success)  # Deadlock if Banker's failed
        fragmentation_results['First Fit'].append(sum(allocator.memory_blocks))  # Remaining memory

        # Best Fit
        start_time = time.time()
        best_fit_success = allocator.best_fit(process_size)
        end_time = time.time()
        runtime_results['Best Fit'].append(end_time - start_time)
        allocation_results['Best Fit'].append(best_fit_success)
        deadlock_results['Best Fit'].append(not best_fit_success)  # Deadlock if allocation failed
        fragmentation_results['Best Fit'].append(sum(allocator.memory_blocks))

        # Worst Fit
        start_time = time.time()
        worst_fit_success = allocator.worst_fit(process_size)
        end_time = time.time()
        runtime_results['Worst Fit'].append(end_time - start_time)
        allocation_results['Worst Fit'].append(worst_fit_success)
        deadlock_results['Worst Fit'].append(not worst_fit_success)
        fragmentation_results['Worst Fit'].append(sum(allocator.memory_blocks))

    return allocation_results, fragmentation_results, runtime_results, deadlock_results

# =========================
# Plotting Function
# =========================
def plot_results(allocation_results, fragmentation_results, runtime_results, deadlock_results, scenario_number):
    # --- Allocation Success & Fragmentation ---
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    x = list(range(1, len(next(iter(allocation_results.values()))) + 1))  # Request numbers

    y_allocation = [0, 1, 2]  # Y positions for each strategy
    y_fragmentation = [0, 1, 2]

    colors = ['b', 'g', 'r']  # Blue, Green, Red
    markers = ['o', 's', '^']

    # Plot allocation success for each strategy
    for i, (strategy, color, marker) in enumerate(zip(allocation_results.keys(), colors, markers)):
        ax.plot(x, [y_allocation[i]] * len(allocation_results[strategy]), allocation_results[strategy],
                label=f'{strategy} Success', marker=marker, color=color, linewidth=3)

    # Plot fragmentation for each strategy
    for i, (strategy, color, marker) in enumerate(zip(fragmentation_results.keys(), colors, markers)):
        ax.plot(x, [y_fragmentation[i]] * len(fragmentation_results[strategy]), fragmentation_results[strategy],
                label=f'{strategy} Fragmentation', linestyle='--', marker=marker, color=color, linewidth=3)

    ax.set_xlabel('Request Number', fontsize=11)
    ax.set_ylabel('Type', fontsize=11)
    ax.set_zlabel('Count', fontsize=11)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Allocation Success', 'Fragmentation'], fontsize=11)
    ax.set_title(f'3D Line Graph of Memory Allocation Success and Fragmentation (Scenario {scenario_number})', fontsize=18)
    ax.legend(fontsize=11)
    ax.grid(True)
    plt.show()

    # --- Runtime & Deadlock Occurrence ---
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot runtime for each strategy
    for i, (strategy, color, marker) in enumerate(zip(runtime_results.keys(), colors, markers)):
        ax.plot(x, [3 + i] * len(runtime_results[strategy]), runtime_results[strategy],
                label=f'{strategy} Runtime', marker=marker, color=color, linewidth=3)

    # Plot deadlock occurrence for each strategy
    for i, (strategy, color, marker) in enumerate(zip(deadlock_results.keys(), colors, markers)):
        ax.plot(x, [3 + i + 0.5] * len(deadlock_results[strategy]), deadlock_results[strategy],
                label=f'{strategy} Deadlock', linestyle='--', marker=marker, color=color, linewidth=3)

    ax.set_xlabel('Request Number', fontsize=11)
    ax.set_ylabel('Type', fontsize=11)
    ax.set_zlabel('Value', fontsize=11)
    ax.set_yticks([3, 4, 5])
    ax.set_yticklabels(['First Fit Runtime', 'Best Fit Runtime', 'Worst Fit Runtime'], fontsize=11)
    ax.set_title(f'3D Line Graph of Runtime and Deadlock Occurrence (Scenario {scenario_number})', fontsize=18)
    ax.legend(fontsize=11)
    ax.grid(True)
    plt.show()

# =========================
# Results Printing Function
# =========================
def print_results(allocation_results, fragmentation_results, runtime_results, deadlock_results):
    # Print allocation results
    print("Allocation Success:")
    for strategy, results in allocation_results.items():
        print(f"{strategy}: {results}")
    print("\nMemory Fragmentation:")
    for strategy, results in fragmentation_results.items():
        print(f"{strategy}: {results}")

    # Print runtime and deadlock results
    print("\nRuntime Results:")
    for strategy, results in runtime_results.items():
        print(f"{strategy}: {results}")
    print("\nDeadlock Occurrence Results:")
    for strategy, results in deadlock_results.items():
        print(f"{strategy}: {results}")

    # Analysis
    total_requests = len(allocation_results['First Fit'])
    successful_allocations = {strategy: sum(results) for strategy, results in allocation_results.items()}
    print("\nAnalysis of Results:")
    for strategy, success_count in successful_allocations.items():
        print(f"{strategy} succeeded in {success_count} out of {total_requests} requests.")
        success_rate = (success_count / total_requests) * 100
        print(f"Success Rate for {strategy}: {success_rate:.2f}%")

# =========================
# Main Simulation Runner
# =========================
if __name__ == "__main__":
    # Define scenarios for simulation
    scenarios = [
        # Scenario 1: All Allocations Succeed, low resource/memory usage
        [([1, 0, 1], 80), ([1, 1, 0], 90), ([0, 1, 1], 70), ([1, 0, 1], 60), ([0, 1, 0], 50)],
        # Scenario 2: Some Allocations Fail due to memory/resource exhaustion
        [([2, 2, 2], 400), ([3, 1, 0], 250), ([1, 2, 1], 300), ([2, 0, 2], 200), ([2, 1, 2], 350)],
        # Scenario 3: Deadlock Occurs (requests exceed available, circular wait)
        [([2, 1, 2], 200), ([2, 2, 2], 250), ([2, 2, 2], 300), ([2, 1, 2], 150), ([2, 2, 2], 100)],
        # Scenario 4: Mixed Outcomes (some succeed, some fail, some fragment)
        [([1, 0, 2], 210), ([2, 0, 0], 140), ([3, 1, 1], 310), ([1, 2, 1], 120), ([0, 1, 2], 180)],
        # Scenario 5: All Failures (requests too large for available resources/memory)
        [([5, 5, 5], 700), ([6, 4, 6], 800), ([7, 5, 7], 900), ([8, 6, 8], 1000), ([9, 7, 9], 1100)],
        # Scenario 6: Fragmentation Test (small requests after large allocations)
        [([3, 0, 2], 500), ([2, 2, 1], 400), ([1, 1, 1], 50), ([1, 0, 1], 60), ([0, 1, 0], 40)],
    ]

    # Run each scenario and collect results
    for i, scenario in enumerate(scenarios):
        print(f"\nRunning Scenario {i + 1}:")
        allocation_results, fragmentation_results, runtime_results, deadlock_results = simulate_memory_allocation_and_deadlock(scenario)
        print_results(allocation_results, fragmentation_results, runtime_results, deadlock_results)
        plot_results(allocation_results, fragmentation_results, runtime_results, deadlock_results, i + 1)
