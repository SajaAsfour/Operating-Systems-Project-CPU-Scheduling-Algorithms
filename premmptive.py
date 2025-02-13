#saja asfour 
#1210737
#sec2
from collections import deque, defaultdict

class Process:
    def __init__(self, ProcessId, ArrivalTime, priority, CpuBurstTime, IOBurstTime):
        self.ProcessId = ProcessId
        self.ArrivalTime = ArrivalTime
        self.priority = priority
        self.CpuBurstTime = CpuBurstTime
        self.IOBurstTime = IOBurstTime
        self.remaining_cpu = CpuBurstTime
        self.waiting_time = 0
        self.turnaround_time = 0
        self.time_in_ready_queue = 0

class Scheduler:
    def __init__(self):
        #Initializes the current time of the scheduler to 0
        self.time = 0
        #Sets the time quantum for the round-robin scheduling
        self.q = 2
        #Initializes a deque for the new processes that arrive but are not yet ready to execute
        self.new_queue = deque()
        #Initializes a dictionary of deques, where each deque corresponds to a priority level
        self.ready_queues = defaultdict(deque)  #defaultdict(deque) ensures that if a key (priority level) does not exist, it will automatically create a new deque for that key
        #Initializes a deque for processes that are waiting for I/O operations to complete
        self.waiting_queue = deque()
        self.current_process = None  # Track the currently running process
        #Initializes an empty list to store processes that have completed their execution
        self.finished_processes = []

    def add_process(self, process):
        self.new_queue.append(process)

    def execute(self, max_time):
        #loop ensures that the scheduler runs until it reaches the specified max_time
        while self.time < max_time:
            # checks if there are new processes whose arrival time is less than or equal to the current time
            while self.new_queue and self.new_queue[0].ArrivalTime <= self.time:
                process = self.new_queue.popleft()
                self.ready_queues[process.priority].append(process)

            # Aging mechanism: decrement priority if in ready queue for 5 time units
            for priority in sorted(self.ready_queues.keys()):
                #loop iterates over all priorities in ready_queues
                for process in list(self.ready_queues[priority]):
                    #For each process in each priority queue, it increments time_in_ready_queue
                    process.time_in_ready_queue += 1
                    #If a process has been in the ready queue for 5 time units
                    if process.time_in_ready_queue >= 5:
                        #its priority is decremented, and it is moved to the appropriate priority queue
                        self.ready_queues[priority].remove(process)
                        process.priority -= 1
                        process.time_in_ready_queue = 0
                        self.ready_queues[process.priority].append(process)

                        #if the process’s priority equals the current process’s priority
                        if self.current_process and process.priority == self.current_process.priority:
                            #the current process is preempted
                            self.ready_queues[self.current_process.priority].append(self.current_process)
                            self.current_process = None

            # Find the highest priority process to execute
            #identifies the highest priority available
            highest_priority = min(self.ready_queues.keys(), default=None)
            if highest_priority is not None:
                # If there is no current process or the current process is of lower priority, preempt it
                if self.current_process is None or highest_priority < self.current_process.priority:
                    if self.current_process is not None:
                        # Preempt the current process
                        self.ready_queues[self.current_process.priority].append(self.current_process)
                    self.current_process = self.ready_queues[highest_priority].popleft()
                    self.current_process.time_in_ready_queue = 0  # Reset the time in ready queue
                    print(f" {self.time} | P{self.current_process.ProcessId} | ",end="")

            # Round Robin for processes with the same highest priority
            if self.current_process:
                execution_time = min(self.q, self.current_process.remaining_cpu, max_time - self.time)
                for t in range(execution_time):
                    self.time += 1
                    #decreases the remaining CPU burst time
                    self.current_process.remaining_cpu -= 1

                    # If a new process arrives with a higher priority, the current process is preempted
                    if self.new_queue and self.new_queue[0].ArrivalTime <= self.time and self.new_queue[0].priority < self.current_process.priority:
                        self.ready_queues[self.current_process.priority].append(self.current_process)
                        self.current_process = None
                        break

                    #When the current process’s CPU burst is completed 
                    if self.current_process.remaining_cpu == 0:
                        #it is moved to the waiting queue, and its turnaround and waiting times are calculated
                        self.current_process.turnaround_time = self.time - self.current_process.ArrivalTime
                        self.current_process.waiting_time += self.current_process.turnaround_time - self.current_process.CpuBurstTime
                        self.current_process.remaining_cpu = self.current_process.CpuBurstTime
                        self.current_process.waiting_time = self.time + self.current_process.IOBurstTime
                        self.waiting_queue.append(self.current_process)
                        self.finished_processes.append(self.current_process)
                        self.current_process = None
                        break
                #If the current process still has remaining CPU time after the time slice 
                if self.current_process and self.current_process.remaining_cpu > 0:
                    #if there are higher priority processes in the ready queue
                    if highest_priority is not None and len(self.ready_queues[highest_priority]) > 0:
                        #the process is preempted and moved to the end of its priority queue
                        self.ready_queues[self.current_process.priority].append(self.current_process)
                        self.current_process = None

            # Check if any processes in the waiting queue are ready to move to the ready queue
            while self.waiting_queue and self.waiting_queue[0].waiting_time <= self.time:
                process = self.waiting_queue.popleft()
                self.ready_queues[process.priority].append(process)
            
            #If nothing is happening(no processes are in the queues or currently running),incremant the time
            if not self.new_queue and not any(self.ready_queues.values()) and not self.current_process:
                self.time += 1

        # Calculate and print average waiting time and average turnaround time
        total_waiting_time = 0
        total_turnaround_time = 0
        num_processes = len(self.finished_processes)

        #find the total waiting time amd total turmaround time
        for process in self.finished_processes:
            total_waiting_time += process.waiting_time
            total_turnaround_time += process.turnaround_time
        
        #calculate the average
        avg_waiting_time = total_waiting_time / num_processes if num_processes else 0
        avg_turnaround_time = total_turnaround_time / num_processes if num_processes else 0

        print(f"{self.time}") #this for last time in gantt chart
        print(f"\n\nAverage Waiting Time for preemptive scheduling: {avg_waiting_time}")
        print(f"Average Turnaround Time for preemptive scheduling : {avg_turnaround_time}")

if __name__ == "__main__":
    scheduler = Scheduler()
    processes = [
        Process(1, 0, 3, 15, 5),
        Process(2, 1, 2, 23, 14),
        Process(3, 3, 3, 14, 6),
        Process(4, 4, 1, 16, 15),
        Process(5, 6, 0, 10, 13),
        Process(6, 7, 1, 22, 4),
        Process(7, 8, 2, 28, 10)
    ]
    
    for process in processes:
        scheduler.add_process(process)
    
    print("\nGantt chart for Premmptive scheduling:\n")
    scheduler.execute(300)
