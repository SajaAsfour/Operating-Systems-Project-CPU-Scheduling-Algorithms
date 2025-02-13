#saja asfour 
#1210737
#sec2
import heapq
from collections import deque


class Process:
    def __init__(self, ProcessId, ArrivalTime, CpuBurstTime, IOBurstTime, priority):

        #attribute of the class
        self.ProcessId = ProcessId
        self.ArrivalTime = ArrivalTime
        self.CpuBurstTime = CpuBurstTime
        self.IOBurstTime = IOBurstTime
        self.priority = priority
        self.remaining_burst = CpuBurstTime
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0

        # 0 for Q0, 1 for Q1, 2 for Q2
        #Q0– RR with time q 8 
        #Q1- RR time q 16 
        #Q2-FCFS
        self.current_queue = 0 

        self.last_executed_time = 0      # Last time it was executed

    #ensuring that the processes are correctly ordered when they are stored in a priority queue implemented with heapq.
    def __lt__(self, other):
        return self.ArrivalTime < other.ArrivalTime

# Multilevel Feedback Queue Scheduler
class MLFQScheduler:

    def __init__(self, time_limit):

        self.time = 0       #Initializes the current time of the scheduler to 0(This is the starting point of the simulation)
        self.time_limit = time_limit
        #Initializes three deques to represent the three different queues 
        #(Q0, Q1, Q2) used in the Multilevel Feedback Queue scheduling
        self.queues = [deque(), deque(), deque()]  
        #Initializes a deque to represent the waiting queue for processes that are currently in their I/O burst phase
        self.WaitingQueue = deque()
        #empty list to store the processes ,before being moved to the appropriate ready queue based on their arrival time
        self.processes = [] 
        #empty list to store the Gantt chart        
        self.gantt_chart = []
        #empty list to store processes that have completed their CPU burst
        self.completed_processes = []

    #add processes in a priority queue based on their arrival times.
    def add_process(self, process):
        heapq.heappush(self.processes, process)

    def ALGO(self):
        #to ensure that we have period 300
        while self.time < self.time_limit:

            # Check if there is new process come inside the period
            while self.processes and self.processes[0].ArrivalTime <= self.time:

                #removes and returns the process with the smallest arrival time
                process = heapq.heappop(self.processes)
                #add process to the multilevel queue
                self.queues[0].append(process)

            # Move processes from waiting queue to ready queue if I/O burst is done
            for process in list(self.WaitingQueue):
                #if I/O burst  for the process is done
                if self.time - process.last_executed_time >= process.IOBurstTime:
                    #remove process from waiting queue
                    self.WaitingQueue.remove(process)
                    #update the remaining process to be again the cpu burst time for the process
                    process.remaining_burst = process.CpuBurstTime
                    #add process to the multilevel queue
                    self.queues[0].append(process)

            #iterates over the indices of three queues which process tasks in each queue sequentially
            for index in range(3):

                #checks if the current queue (index) has any processes waiting to be executed
                if self.queues[index]:
                    #for Q0 --> q=8
                    if index == 0:
                        q = 8
                    #for Q1--> q=16
                    elif index == 1:
                        q = 16
                    #for Q2 --> FCFS
                    else:
                        q = self.time_limit - self.time  # Essentially unlimited for FCFS

                    # remove the process from the front of the current queue anc set it to process
                    process = self.queues[index].popleft()

                    #to calculate the average waiting time
                    if process.waiting_time == 0:
                        process.waiting_time = self.time - process.ArrivalTime

                    #time allocated to the process is the smaller of its remaining burst time and the quantum
                    executed_time = min(process.remaining_burst, q)

                    self.gantt_chart.append((self.time, self.time + executed_time, process.ProcessId))
                    process.remaining_burst -= executed_time
                    self.time += executed_time

                    #If the process has finished its cpu burst time
                    if process.remaining_burst == 0:
                        process.completion_time = self.time
                        process.turnaround_time = process.completion_time - process.ArrivalTime
                        self.completed_processes.append(process)
                        process.last_executed_time = self.time
                        #add it to waiting queue
                        self.WaitingQueue.append(process) 
                    #if the process does not completed yet
                    else:
                        process.last_executed_time = self.time
                        #this if process in Q0 or Q1
                        if index < 2:
                            #moved to the next queue
                            process.current_queue = index + 1
                            self.queues[process.current_queue].append(process)
                        #if it is in Q2
                        else:
                            #remains in the same queue
                            self.queues[2].append(process)
                    break
            #If no queue had processes, the time is incremented by 1
            else:
                self.time += 1

    #compute the average waiting time and average turnaround time for a set of completed processes
    def CalculateTheTime(self):
        total_waiting_time = 0
        total_turnaround_time = 0
        num_processes = len(self.completed_processes)
        #print("\n")
        #for p in self.completed_processes:
            #print(f"For {p.ProcessId}: Waiting Time = {p.waiting_time} And Turnaround Time = {p.turnaround_time}")

        for process in self.completed_processes:
            total_waiting_time += process.waiting_time
            total_turnaround_time += process.turnaround_time

        if num_processes>0:
            avg_waiting_time = total_waiting_time / num_processes 
            avg_turnaround_time = total_turnaround_time / num_processes 
        else :
            avg_waiting_time=0
            avg_turnaround_time=0

        return avg_waiting_time, avg_turnaround_time

    def print_gantt_chart(self):
        print("\nGantt Chart For MultiLevel Queue:\n")
        for start, end, process in self.gantt_chart:
            if end>300:
                end=300
            print(f"{process}({start}-{end})|",end="")

# Initialize the processes
processes = [
    Process("P1", 0, 15, 5, 3),
    Process("P2", 1, 23, 14, 2),
    Process("P3", 3, 14, 6, 3),
    Process("P4", 4, 16, 15, 1),
    Process("P5", 6, 10, 13, 0),
    Process("P6", 7, 22, 4, 1),
    Process("P7", 8, 28, 10, 2)
]

scheduler = MLFQScheduler(300)

for process in processes:
    scheduler.add_process(process)

scheduler.ALGO()
scheduler.print_gantt_chart()
avg_waiting_time, avg_turnaround_time = scheduler.CalculateTheTime()
print(f"\n\nAverage Waiting Time For MultiLevel Queue: {avg_waiting_time}")
print(f"Average Turnaround Time For MultiLevel Queue: {avg_turnaround_time}")
