#saja asfour 
#1210737
#sec2
from collections import deque
# Process structure
class Process:

    def __init__(self, ProcessId, ArrivalTime, CpuBurstTime, IOBurstTime, priority):
        #process attribute
        self.ProcessId = ProcessId          
        self.ArrivalTime = ArrivalTime
        self.CpuBurstTime = CpuBurstTime
        self.remaining_burst = CpuBurstTime     # the remaminig cpu burst time that does not execute(initially it is equall to cpu burst time)
        self.IOBurstTime = IOBurstTime
        self.priority = priority
        self.start_time = None                  
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0

# define the processes (list of tubel)
Process = [
    Process("P1", 0, 15, 5, 3),
    Process("P2", 1, 23, 14, 2),
    Process("P3", 3, 14, 6, 3),
    Process("P4", 4, 16, 15, 1),
    Process("P5", 6, 10, 13, 0),
    Process("P6", 7, 22, 4, 1),
    Process("P7", 8, 28, 10, 2)
]

# Sort processes by arrival time
Process.sort(key=lambda x: x.ArrivalTime)

# Ready queue, IO queue and priority-based RR queues

ReadyQueue = deque()        #hold processes ready for CPU execution
WaitingQueue = []           #stores processes that are waiting for I/O completion
priority_queues = {}        #dictionary where each key corresponds to a priority level 
                            #and its value is a deque holding processes of that priority level
                            #allowing for round-robin scheduling within each priority level

time = 0                    #the timer start from zero 
q = 2                       #quntum
gantt_chart = []            #to print the gannt chart


# Add processes to ready queue based on arrival time
def AddProcess():

    # i make time golbal to ensures that any modifications to time inside 
    #the function affect the global variable directly
    global time
    while Process and Process[0].ArrivalTime <= time:
        
        process = Process.pop(0)        #removes and returns the element at index 0 from the list Process

        #add process to priority queue based on its priority
        if process.priority not in priority_queues:

            priority_queues[process.priority] = deque()

        priority_queues[process.priority].append(process)

# Update IO queue and move processes back to ready queue if their IO burst is done
def update_WaitingQueue():

    # i make time golbal to ensures that any modifications to time inside 
    #the function affect the global variable directly
    global time
    index = 0       #index to iterate over the WaitingQueue

    #iterates through the elements of WaitingQueu
    while index < len(WaitingQueue):

        process, return_time = WaitingQueue[index]          #Retrieves the tuple (process, return_time) from WaitingQueue at index
        
        #checks if the process has finished waiting and can now be moved to its respective priority queue 
        if return_time <= time:

            priority_queues[process.priority].append(process)
            WaitingQueue.pop(index)

        else:

            index += 1

# Select the next process to execute based on priority
def SelectNextProcess():

    for priority in sorted(priority_queues.keys()): #sorts the keys (priority levels) in ascending order

        #checks if the current priority queue has any processes
        if priority_queues[priority]:

            #returns the current state of the queue if it still has processes left, otherwise it returns None
            return priority_queues[priority].popleft(), priority_queues[priority] if len(priority_queues[priority]) > 0 else None

    #If no processes are found in any of the priority queues, the function returns (None, None)   
    return None, None  # No processes found in any priority queue (CurrentProcess, RRQueue  both will be null)

# Execute processes based on priority and RR for 300 time units
while time < 300:

    AddProcess()
    update_WaitingQueue()
    
    CurrentProcess, RRQueue = SelectNextProcess()  
    
    if CurrentProcess:

        #It runs for the full remaining burst time if no other processes are waiting
        # and  runs for the smaller of the time quantum or the remaining burst time if there are other processes waiting   
        execution_time = CurrentProcess.remaining_burst if RRQueue is None else min(q, CurrentProcess.remaining_burst)
        #append the process that finish execute to gannt chart
        gantt_chart.append((time, CurrentProcess.ProcessId, execution_time))
        
        if CurrentProcess.start_time is None:

            CurrentProcess.start_time = time
        
        CurrentProcess.remaining_burst -= execution_time
        time += execution_time      #update the timer 
        
        # If the current process still has burst time left, it needs to be re-added to an appropriate queue
        if CurrentProcess.remaining_burst > 0:
            #if the current process was not in the Round Robin queue
            if RRQueue is None:
                #so it should be re-added to its priority queue.
                priority_queues[CurrentProcess.priority].append(CurrentProcess)

            #if there are more processes in the Round Robin queue
            else:
                #re-adds the process to the Round Robin queue
                RRQueue.append(CurrentProcess)
        
        #if the process has finished its current CPU burst
        else:
            #Reset the process's remaining burst time for its next cycle
            CurrentProcess.remaining_burst = CurrentProcess.CpuBurstTime 
            #Move the process to the I/O waiting queue with its I/O burst time
            WaitingQueue.append((CurrentProcess, time + CurrentProcess.IOBurstTime))
            #Update the process's completion time for the current cycle
            CurrentProcess.completion_time = time  
            #Update the process's turnaround time, which is the total time taken from arrival to completion
            CurrentProcess.turnaround_time += time - CurrentProcess.start_time

    #If no process is ready to execute
    #the system clock needs to advance to the next significant event 
    #(either the arrival of a new process or the completion of an I/O operation).
    else:
        #If there is a process that has arrived
        if Process:
            #advance time to the arrival time of the next process
            time = Process[0].ArrivalTime
        #If there are processes in the I/O waiting queue
        elif WaitingQueue:
            #advance time to the earliest I/O completion time
            time = min(WaitingQueue, key=lambda x: x[1])[1]

# Print Gantt Chart
print("Gantt Chart For Non_preemptive:")
DisplayGanttChart = ""

for start, ProcessId, Duration in gantt_chart:
    #to ensure to stop at period =300
    if start+Duration >300:
        DisplayGanttChart += f"|{ProcessId}({start}-{300})"
    else:
        DisplayGanttChart += f"|{ProcessId}({start}-{start+Duration})"

DisplayGanttChart += "|"

print(DisplayGanttChart)

# Calculate average waiting time and average turnaround time
total_waiting_time = 0
total_turnaround_time = 0
num_processes = 7  # There are 7 initial processes

# Collect all processes for calculation

#his list comprehension gathers all processes from the priority_queues dictionary 
#It iterates through each queue in the dictionary and collects all processes in those queues
all_processes = [p for q in priority_queues.values() for p in q]

#iterates through the WaitingQueue, collecting processes that are waiting for I/O operations
for process, _ in WaitingQueue:
    #extracts each process from the tuples in the WaitingQueue and appends them to all_processes
    all_processes.append(process)

#terates through all collected processes to calculate their waiting time and turnaround time
for process in all_processes:
    #checks if the process has a recorded completion time
    if process.completion_time :
        #the process has finished execution, and its metrics can be calculated
        turnaround_time = process.completion_time - process.ArrivalTime
        waiting_time = turnaround_time - process.CpuBurstTime
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        print(f"For {process.ProcessId} in Non_preemptive: Waiting Time = {waiting_time} And Turnaround Time = {turnaround_time}")
    

    average_waiting_time = total_waiting_time / num_processes
    average_turnaround_time = total_turnaround_time / num_processes

print(f"\nAverage Waiting Time For Non_preemptive: {average_waiting_time}")
print(f"Average Turnaround Time For Non_preemptive: {average_turnaround_time}")
