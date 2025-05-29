## Simulating and Analyzing Deadlock and Memory Allocation Strategies in Operating Systems

Deadlock is a situation in computing where multiple processes are unable to proceed because each is waiting for a resource held by another, leading to a complete system standstill. For a deadlock to occur, four conditions must exist simultaneously—known as the Coffman conditions:

1. **Mutual Exclusion**: Resources cannot be shared.
2. **Hold and Wait**: A process holds one resource while waiting for another.
3. **No Preemption**: Resources cannot be forcibly taken from processes.
4. **Circular Wait**: A closed chain of processes exists, where each process waits for a resource held by the next.

Understanding these conditions is key to analyzing and preventing deadlocks in system design.

Deadlocks can be **detected** using techniques such as wait-for graphs or by checking for circular wait conditions. Once detected, systems can **recover** by terminating processes, preempting resources, or rolling back to a safe state.

**Prevention** strategies aim to eliminate at least one Coffman condition. For instance:
- Requiring all resources to be requested at once (avoiding hold and wait),
- Using algorithms like the **Banker's Algorithm** to ensure the system remains in a safe state before allocating resources.

These approaches are especially important in environments requiring high reliability and uptime, such as real-time or distributed systems. If left unaddressed, deadlocks can degrade system performance, cause application crashes, or lead to data loss. In distributed systems, the absence of a centralized resource manager makes deadlocks even more complex to handle.

Therefore, **proactive deadlock testing and simulation** are crucial during system development. Overall, robust deadlock management through detection, prevention, and recovery—is essential for maintaining efficient and stable computing environments across all types of operating systems.
## Team Member Names and Roles

| Member Name              | Contribution                                                        |
|--------------------------|----------------------------------------------------------------------|
| Mark Andrie Atienza      | README, Report Writing                                               |
| John Lance Baljon        | Proofreading, Testing & Support, Final Polishing                    |
| Joshua Vincent Bernardino| Theory, Programming, & Algorithm Implementation                     |
| Ma. Margaret Fundano     | Presentation Creation, Video Editing, Documentation, Proofreading   |
| Joven Serrano            | Data Analysis, Report Writing                                       |


---

## 📸 Sample Output Screenshots & Code Explanation

### 🧠 Code Overview

This project simulates **deadlock detection** and **memory allocation efficiency** using classical operating system algorithms implemented in Python.

---

### 🔍 Banker's Algorithm

The `BankersAlgorithm` class is used for simulating **deadlock avoidance**:

* `request_resources(process_id, request)`
  → Allocates resources if the request does not lead to an unsafe state.
* `is_safe()`
  → Simulates whether the current state is safe using the Work and Finish vectors.

**Deadlock is avoided** by allowing resource allocation only if the system remains in a safe state after granting the request.

---

### 💾 Memory Allocation Strategies

Implemented in the `MemoryAllocator` class, the simulation uses:

* **First Fit**: Allocates the first block large enough for the process.
* **Best Fit**: Chooses the smallest available block that fits the process.
* **Worst Fit**: Chooses the largest block to potentially minimize fragmentation.

Each strategy returns a boolean for success and updates memory block sizes.

---

### 🔁 Simulation Process

For each scenario:

* A **Banker's Algorithm** instance manages resource requests.
* Memory is allocated using **First Fit**, **Best Fit**, and **Worst Fit**.
* **Metrics Tracked**:

  * Allocation success
  * Memory fragmentation
  * Deadlock occurrence
  * Runtime (execution time)

---

### 📊 Sample Results (Scenario 1)

```bash
Running Scenario 1:
Allocation Success:
First Fit: [True, True, True]
Best Fit: [True, True, True]
Worst Fit: [True, True, False]

Memory Fragmentation:
[1100, 650, 290]

Deadlock Occurrence:
First Fit: [True, True, True]
Best Fit: [False, False, False]
Worst Fit: [False, False, True]

Success Rates:
First Fit: 100%
Best Fit: 100%
Worst Fit: 66.67%
```

---

### 📈 Sample Output Graphs

#### ✅ Allocation & Fragmentation (Scenario 1)

![Allocation Fragmentation](img/scenario1_allocation_fragmentation.jpg)

#### ❌ Deadlock & Runtime (Scenario 1)

![Deadlock Runtime](img/scenario1_deadlock_runtime.jpg)

> **Legend**:
>
> * **Solid lines**: Allocation / Runtime
> * **Dashed lines**: Fragmentation / Deadlock Occurrence

---

### 📌 Observations Across Scenarios

| Strategy  | Avg Success Rate | Deadlock Resistance | Fragmentation Handling | Runtime Stability |
| --------- | ---------------- | ------------------- | ---------------------- | ----------------- |
| First Fit | High             | Poor                | Worst                  | Stable            |
| Best Fit  | High             | Excellent           | Best                   | Stable            |
| Worst Fit | Moderate         | Inconsistent        | Moderate               | Stable            |

---

### 🏆 Best Performing Strategy

**✅ Best Fit**
✔ High allocation success
✔ Lowest deadlock occurrence
✔ Efficient fragmentation handling
✔ Scales well under pressure

---

### 📂 How to Use

```bash
# Run the simulation
python memory_simulation.py
```

Ensure the required library is installed:

```bash
pip install matplotlib
