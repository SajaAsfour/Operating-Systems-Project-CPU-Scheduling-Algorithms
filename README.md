# ⏳ Operating Systems Project - CPU Scheduling Algorithms

## 📌 Overview
This repository contains my implementation of **Project 2 for the Operating Systems (ENCS3390) course at Birzeit University**. The project focuses on simulating and analyzing three different **CPU scheduling algorithms**:
1. **Preemptive Priority Scheduling**
2. **Non-Preemptive Priority Scheduling**
3. **Multilevel Feedback Queue (MLFQ) Scheduling**

The goal is to compare their performance in terms of **waiting time, turnaround time, and CPU utilization**.

## 🛠 Features
- ✅ **Preemptive Priority Scheduling (`premmptive.py`)**
  - Uses **priority-based** round-robin scheduling.
  - Implements **aging** to prevent starvation.
  - Supports process preemption based on arrival and priority.
  - Generates a **Gantt chart** for process execution.
- ✅ **Non-Preemptive Priority Scheduling (`nonPremmptive.py`)**
  - Executes processes based on **static priority**.
  - No preemption once a process starts execution.
  - Uses **round-robin scheduling** within the same priority level.
- ✅ **Multilevel Feedback Queue (MLFQ) Scheduling (`multi.py`)**
  - Implements a **3-level queue** with different scheduling policies:
    - **Q0:** Round Robin (Time Quantum = 8)
    - **Q1:** Round Robin (Time Quantum = 16)
    - **Q2:** First-Come, First-Served (FCFS)
  - Dynamically moves processes between queues based on CPU burst behavior.
  - Supports **priority-based aging** to optimize execution fairness.

## 📂 Contents
- 📜 **premmptive.py:** Preemptive Priority Scheduling implementation.
- 📜 **nonPremmptive.py:** Non-Preemptive Priority Scheduling implementation.
- 📜 **multi.py:** Multilevel Feedback Queue Scheduling implementation.
- 📄 **Project Report (output.pdf):**
  - Detailed explanation of algorithms.
  - Gantt charts for each scheduling method.
  - Performance evaluation & comparisons.

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/SajaAsfour/Operating-Systems-Project-CPU-Scheduling-Algorithms
   ```
2. Run any scheduling algorithm:
   ```bash
   python premmptive.py
   ```
   ```bash
   python nonPremmptive.py
   ```
   ```bash
   python multi.py
   ```
3. Observe the **Gantt chart** and **average waiting/turnaround times**.
4. Compare results to determine the best scheduling policy.

## 📌 Requirements
- Python 
- Basic knowledge of CPU scheduling algorithms & process management

## 👩‍💻 Author
**Saja Asfour**
- 🎓 Computer Engineering Student at Birzeit University
- 🏠 GitHub: [SajaAsfour](https://github.com/SajaAsfour)

## 📜 License
This repository is for educational purposes. Feel free to use and reference the work, but please give proper credit. 😊
