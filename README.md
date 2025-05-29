# 🖥️ OS Deadlock & Memory Allocation Simulator

A Python project to **simulate, visualize, and analyze deadlock avoidance and memory allocation strategies** in operating systems. This tool demonstrates how the Banker's Algorithm and classic memory allocation methods (First Fit, Best Fit, Worst Fit) behave under various process workloads, helping students and engineers understand resource management and deadlock prevention.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Key Concepts](#key-concepts)
- [How It Works](#how-it-works)
- [Sample Output](#sample-output)
- [Strategy Comparison](#strategy-comparison)
- [How to Run](#how-to-run)
- [Team Members](#team-members)
- [License](#license)

---

## 📝 Overview

This project models how an operating system manages resources and memory for multiple processes, focusing on:

- **Deadlock avoidance** using the Banker's Algorithm.
- **Memory allocation** using First Fit, Best Fit, and Worst Fit strategies.
- **Visualization** of allocation success, fragmentation, deadlock occurrence, and runtime for each strategy and scenario.

You can run multiple scenarios to observe how different strategies perform under varying workloads and resource demands.

---

## 📚 Key Concepts

### 💥 Deadlock in Operating Systems

A **deadlock** occurs when processes are stuck waiting for each other’s resources, causing the system to halt. The four Coffman conditions for deadlock are:

1. **Mutual Exclusion**: Resources are non-shareable.
2. **Hold and Wait**: Processes hold resources while waiting for others.
3. **No Preemption**: Resources cannot be forcibly taken.
4. **Circular Wait**: A cycle of processes exists, each waiting for the next.

**Deadlock avoidance** is critical for system reliability, especially in real-time and distributed systems.

---

### 🏦 Banker's Algorithm

The **Banker's Algorithm** checks if granting a resource request keeps the system in a safe state. If not, the request is denied to avoid deadlock.

- `request_resources(process_id, request)`: Allocates resources if safe.
- `is_safe()`: Checks if the system remains in a safe state after allocation.

---

### 💾 Memory Allocation Strategies

Implemented in the `MemoryAllocator` class:

- **First Fit**: Allocates the first block large enough.
- **Best Fit**: Allocates the smallest suitable block.
- **Worst Fit**: Allocates the largest available block.

---

## 🔁 How It Works

For each scenario:

1. **Resource requests** and **memory allocations** are simulated for a set of processes.
2. The **Banker's Algorithm** manages resource safety.
3. Memory is allocated using all three strategies.
4. The following metrics are tracked and visualized:
    - Allocation success
    - Memory fragmentation
    - Deadlock occurrence
    - Runtime

---

## 📊 Sample Output

**Console Output:**


**Sample Graphs:**

- **Allocation & Fragmentation (3D Line Plot)**
- **Deadlock & Runtime (3D Line Plot)**

> ![Sample Graph](img/scenario1_allocation_fragmentation.jpg)

---

## 🏆 Strategy Comparison

| Strategy  | Success Rate | Deadlock Resistance | Fragmentation Handling | Runtime Stability |
|-----------|--------------|--------------------|-----------------------|------------------|
| First Fit | High         | Poor               | Worst                 | Stable           |
| Best Fit  | High         | Excellent          | Best                  | Stable           |
| Worst Fit | Moderate     | Inconsistent       | Moderate              | Stable           |

**Best Overall:**  
**Best Fit** — consistently high success, low deadlock, and efficient fragmentation handling.

---

## 🛠️ How to Run

1. **Install dependencies:**
    ```bash
    pip install matplotlib
    ```

2. **Run the simulation:**
    ```bash
    python OS_Final_Deadlock_MemorySim.py
    ```

3. **View results:**  
   - Console output for each scenario  
   - 3D line plots for allocation, fragmentation, deadlock, and runtime

---

## 👥 Team Members

| Name                        | Contribution                                      |
|-----------------------------|---------------------------------------------------|
| Mark Andrie Atienza         | README, Report Writing                            |
| John Lance Baljon           | Proofreading, Testing, Final Polishing            |
| Joshua Vincent Bernardino   | Theory, Programming, Algorithm Implementation     |
| Ma. Margaret Fundano        | Presentation, Video Editing, Documentation        |
| Joven Serrano               | Data Analysis, Report Writing                     |

---

## 📄 License

This project is licensed under the MIT License.  
Feel free to fork, modify, and use this project for your OS studies or research!

---

**Happy Simulating! 🚦**
