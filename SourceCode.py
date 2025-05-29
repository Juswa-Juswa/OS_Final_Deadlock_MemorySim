import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# A class that implements the Banker's Algorithm for deadlock avoidance
class BankersAlgorithm:
    # Constructor to initialize the Banker's Algorithm
    def __init__(self, processes, max_resources, available_resources):
        # Number of processes
        self.processes = processes
        # Maximum resources each process can request
        self.max_resources = max_resources
        # Available resources in the system
        self.available_resources = available_resources
        # Current allocation of resources for each process (initialized to 0)
        self.allocation = [[0] * len(max_resources) for _ in range(processes)]
        # Maximum need of resources for each process (set to half of max_resources for simplicity)
        self.max_need = [[max_resources[i] // 2 for i in range(len(max_resources))] for _ in range(processes)]
        # Current need of resources for each process (calculated as max_need - allocation)
        self.need = [[self.max_need[i][j] - self.allocation[i][j] for j in range(len(max_resources))] for i in range(processes)]

    # Request resources for a given process
    def request_resources(self, process_id, request):
        # Check if the request is valid (does not exceed the need and available resources)
        if all(request[i] <= self.need[process_id][i] for i in range(len(request))) and \
           all(request[i] <= self.available_resources[i] for i in range(len(request))):
            # Allocate resources for the given process
            for i in range(len(request)):
                self.available_resources[i] -= request[i]  # Decrease available resources
                self.allocation[process_id][i] += request[i]  # Increase allocated resources
                self.need[process_id][i] -= request[i]  # Decrease needed resources

            # Check if the system is in a safe state after allocation
            if self.is_safe():
                return True
            else:
                # If not safe, undo the allocation (rollback)
                for i in range(len(request)):
                    self.available_resources[i] += request[i]  # Restore available resources
                    self.allocation[process_id][i] -= request[i]  # Decrease allocated resources
                    self.need[process_id][i] += request[i]  # Restore needed resources
                return False
        # If the request is invalid, return False
        return False

    # Check if the system is in a safe state
    def is_safe(self):
        # Create a copy of the available resources for the safety check
        work = self.available_resources[:]
        # Create a list to keep track of finished processes
        finish = [False] * self.processes
        # Create a list to keep track of the safe sequence
        safe_sequence = []

        # Loop until all processes are finished
        while len(safe_sequence) < self.processes:
            # Check if there is a process that can run
            found = False
            for p in range(self.processes):
                # Check if the process is not finished and can be satisfied with current work
                if not finish[p] and all(self.need[p][i] <= work[i] for i in range(len(work))):
                    # Add the process to the safe sequence
                    for i in range(len(work)):
                        work[i] += self.allocation[p][i]  # Simulate resource allocation
                    finish[p] = True  # Mark the process as finished
                    safe_sequence.append(p)  # Add to safe sequence
                    # Set found to True to indicate a process was found
                    found = True
                    break
            # If there is no process that can run, return False (not safe)
            if not found:
                return False
        # If all processes are finished, return True (safe)
        return True

class MemoryAllocator:
    # Class to manage memory allocation using different algorithms
    def __init__(self, memory_blocks):
        # Initialize the MemoryAllocator with a list of memory blocks
        self.memory_blocks = memory_blocks  # Store the available memory blocks

    def first_fit(self, process_size):
        # Allocate memory using the first fit algorithm
        for i in range(len(self.memory_blocks)):
            # Check if the current block is large enough for the process
            if self.memory_blocks[i] >= process_size:
                # If the current block is large enough, allocate it
                self.memory_blocks[i] -= process_size  # Decrease the size of the memory block
                return True  # Allocation successful
        # If no block is large enough, return False
        return False

    def best_fit(self, process_size):
        # Allocate memory using the best fit algorithm
        best_index = -1  # Initialize best index
        for i in range(len(self.memory_blocks)):
            # Check if the current block is large enough
            if self.memory_blocks[i] >= process_size:
                # If it is, check if it is the best fit so far
                if best_index == -1 or self.memory_blocks[best_index] > self.memory_blocks[i]:
                    best_index = i  # Update best index
        if best_index != -1:
            # If a best fit was found, allocate it
            self.memory_blocks[best_index] -= process_size  # Decrease the size of the best fit block
            return True  # Allocation successful
        # If no block is large enough, return False
        return False

    def worst_fit(self, process_size):
        # Allocate memory using the worst fit algorithm
        worst_index = -1  # Initialize worst index
        for i in range(len(self.memory_blocks)):
            # Check if the current block is large enough
            if self.memory_blocks[i] >= process_size:
                # If it is, check if it is the worst fit so far
                if worst_index == -1 or self.memory_blocks[worst_index] < self.memory_blocks[i]:
                    worst_index = i  # Update worst index
        if worst_index != -1:
            # If a worst fit was found, allocate it
            self.memory_blocks[worst_index] -= process_size  # Decrease the size of the worst fit block
            return True  # Allocation successful
        # If no block is large enough, return False
        return False

def simulate_memory_allocation_and_deadlock(scenario):
    # Simulate memory allocation and deadlock detection for a given scenario
    processes = len(scenario)  # Number of processes matches number of requests
    max_resources = [10, 5, 7]  # Maximum resources for each type
    available_resources = [3, 2, 2]  # Available resources in the system
    banker = BankersAlgorithm(processes, max_resources, available_resources)  # Create an instance of BankersAlgorithm

    memory_blocks = [100, 500, 200, 300, 600]  # Define memory blocks
    allocator = MemoryAllocator(memory_blocks)  # Create an instance of MemoryAllocator

    # Initialize results storage for allocation success and fragmentation
    allocation_results = {
        'First Fit': [],
        'Best Fit': [],
        'Worst Fit': []
    }
    fragmentation_results = {
        'First Fit': [],
        'Best Fit': [],
        'Worst Fit': []
    }

    # Initialize results storage for runtime and deadlock occurrence
    runtime_results = {
        'First Fit': [],
        'Best Fit': [],
        'Worst Fit': []
    }
    deadlock_results = {
        'First Fit': [],
        'Best Fit': [],
        'Worst Fit': []
    }

    # Loop through each process and simulate resource requests and memory allocations
    for process_id, (request, process_size) in enumerate(scenario):
        start_time = time.time()  # Record start time
        allocation_success = banker.request_resources(process_id, request)  # Request resources for the process

        # Attempt to allocate memory using different strategies
        first_fit_success = allocator.first_fit(process_size)
        best_fit_success = allocator.best_fit(process_size)
        worst_fit_success = allocator.worst_fit(process_size)

        end_time = time.time()  # Record end time
        runtime = end_time - start_time  # Calculate runtime

        # Record results of allocation success
        allocation_results['First Fit'].append(first_fit_success)
        allocation_results['Best Fit'].append(best_fit_success)
        allocation_results['Worst Fit'].append(worst_fit_success)

        # Record results of runtime
        runtime_results['First Fit'].append(runtime)
        runtime_results['Best Fit'].append(runtime)
        runtime_results['Worst Fit'].append(runtime)

        # Record results of deadlock occurrence
        deadlock_results['First Fit'].append(not allocation_success)
        deadlock_results['Best Fit'].append(not best_fit_success)
        deadlock_results['Worst Fit'].append(not worst_fit_success)

        # Calculate fragmentation (remaining memory) after each allocation attempt
        fragmentation_results['First Fit'].append(sum(allocator.memory_blocks))
        fragmentation_results['Best Fit'].append(sum(allocator.memory_blocks))
        fragmentation_results['Worst Fit'].append(sum(allocator.memory_blocks))

    return allocation_results, fragmentation_results, runtime_results, deadlock_results

def plot_results(allocation_results, fragmentation_results, runtime_results, deadlock_results, scenario_number):
    # Plot the results of memory allocation success and fragmentation in a 3D line graph
    fig = plt.figure(figsize=(14, 10)) 
    ax = fig.add_subplot(111, projection='3d') 

    # Dynamically set x based on number of requests
    x = list(range(1, len(next(iter(allocation_results.values()))) + 1))

    y_allocation = [0, 1, 2]  
    y_fragmentation = [0, 1, 2]  

    # Define colors and markers for better clarity
    colors = ['b', 'g', 'r']
    markers = ['o', 's', '^']

    # Plotting allocation success for each strategy
    for i, (strategy, color, marker) in enumerate(zip(allocation_results.keys(), colors, markers)):
        ax.plot(x, [y_allocation[i]] * len(allocation_results[strategy]), allocation_results[strategy], 
                label=f'{strategy} Success', marker=marker, color=color, linewidth=3)

    # Plotting fragmentation for each strategy
    for i, (strategy, color, marker) in enumerate(zip(fragmentation_results.keys(), colors, markers)):
        ax.plot(x, [y_fragmentation[i]] * len(fragmentation_results[strategy]), fragmentation_results[strategy], 
                label=f'{strategy} Fragmentation', linestyle='--', marker=marker, color=color, linewidth=3)  

    # Set labels and title for the plot
    ax.set_xlabel('Request Number', fontsize=11)
    ax.set_ylabel('Type', fontsize=11)
    ax.set_zlabel('Count', fontsize=11)
    ax.set_yticks([0, 1])  
    ax.set_yticklabels(['Allocation Success', 'Fragmentation'], fontsize=11)
    ax.set_title(f'3D Line Graph of Memory Allocation Success and Fragmentation (Scenario {scenario_number})', fontsize=18)  
    ax.legend(fontsize=11) 
    ax.grid(True)

    plt.show() 

    # Plot the results of runtime and deadlock occurrence in a 3D line graph
    fig = plt.figure(figsize=(14, 10)) 
    ax = fig.add_subplot(111, projection='3d') 

    # Plotting runtime for each strategy
    for i, (strategy, color, marker) in enumerate(zip(runtime_results.keys(), colors, markers)):
        ax.plot(x, [3 + i] * len(runtime_results[strategy]), runtime_results[strategy], 
                label=f'{strategy} Runtime', marker=marker, color=color, linewidth=3)

    # Plotting deadlock occurrence for each strategy
    for i, (strategy, color, marker) in enumerate(zip(deadlock_results.keys(), colors, markers)):
        ax.plot(x, [3 + i + 0.5] * len(deadlock_results[strategy]), deadlock_results[strategy], 
                label=f'{strategy} Deadlock', linestyle='--', marker=marker, color=color, linewidth=3)  

    # Set labels and title for the plot
    ax.set_xlabel('Request Number', fontsize=11)
    ax.set_ylabel('Type', fontsize=11)
    ax.set_zlabel('Value', fontsize=11)
    ax.set_yticks([3, 4, 5])  
    ax.set_yticklabels(['First Fit Runtime', 'Best Fit Runtime', 'Worst Fit Runtime'], fontsize=11)
    ax.set_title(f'3D Line Graph of Runtime and Deadlock Occurrence (Scenario {scenario_number})', fontsize=18)  
    ax.legend(fontsize=11) 
    ax.grid(True)

    plt.show() 

def print_results(allocation_results, fragmentation_results, runtime_results, deadlock_results):
    # Print the results of memory allocation success and fragmentation
    print("Allocation Success:")
    for strategy, results in allocation_results.items():
        print(f"{strategy}: {results}")  # Print results for each strategy
    print("\nMemory Fragmentation:")
    for strategy, results in fragmentation_results.items():
        print(f"{strategy}: {results}")  # Print fragmentation results for each strategy

    # Print the results of runtime and deadlock occurrence
    print("\nRuntime Results:")
    for strategy, results in runtime_results.items():
        print(f"{strategy}: {results}")  # Print runtime results for each strategy
    print("\nDeadlock Occurrence Results:")
    for strategy, results in deadlock_results.items():
        print(f"{strategy}: {results}")  # Print deadlock occurrence results for each strategy

    # Analyzing results
    total_requests = len(allocation_results['First Fit'])  # Total number of requests
    successful_allocations = {strategy: sum(results) for strategy, results in allocation_results.items()}  # Count successful allocations
    print("\nAnalysis of Results:")
    for strategy, success_count in successful_allocations.items():
        print(f"{strategy} succeeded in {success_count} out of {total_requests} requests.")  # Print success count
        success_rate = (success_count / total_requests) * 100  # Calculate success rate
        print(f"Success Rate for {strategy}: {success_rate:.2f}%")  # Print success rate

if __name__ == "__main__":
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
        allocation_results, fragmentation_results, runtime_results, deadlock_results = simulate_memory_allocation_and_deadlock(scenario)  # Run simulation
        print_results(allocation_results, fragmentation_results, runtime_results, deadlock_results)  # Print results
        plot_results(allocation_results, fragmentation_results, runtime_results, deadlock_results, i + 1)  # Plot results
