import numpy as np
import time
from testSchedulerHelpers import *

CALCUL = "calcul"
IN_OUT = "in out"
INITIALISATION = "initialisation"
CHOOSEN = "choosen"
IN_EXECUTION = "in progress"
COMPLETED = "completed"
BLOCKED = "blocked"
EXEC_TIME_CALCUL = 1
EXEC_TIME_INANDOUT = 3
PP = 1
PAPS = 2


class Queue:
    """
    A class to represent a Queue of processes
    """
    def __init__(self, list_process):
        # Constructs all the necessary attributes for the queue object.
        self.list_process = list_process

    def add_process(self, new_process):
        # Add process to the process list
        self.list_process.append(new_process)

    def sort_processes_by_priority(self):
        """
        :return: A list sorted by priority Desc
        """
        return sorted(self.list_process, key=lambda x: x.priority, reverse=True)

    def init_processes_state(self):
        # All the processes will be initialized with the state 'BLOCKED'
        for p in self.sort_processes_by_priority():
            for t in p.threads:
                t.state = BLOCKED

    def launch(self, policy=PP):
        """
        This method is responsible for starting the simulation
        The simulation will be made according to the chosen policy
        :param policy: Per Priority Without Sarvation or First Come, First Served
        :return:
        """
        self.init_processes_state()
        if policy == PP:
            print(policy)
            number_instruction = 0
            for p in self.list_process:
                number_instruction += (p.nb_instructions_calcul + p.nb_instructions_in_out)
            for _ in range(number_instruction):
                list_process = self.sort_processes_by_priority()
                for t in list_process[0].threads:
                    for i in t.instructions:
                        if i.state == INITIALISATION:
                            self.execute_instruction(i, t)
                            for pr in list_process:
                                if pr != list_process[0]:
                                    pr.priority += 1
                            break
        elif policy == PAPS:
            for p in self.list_process:
                for t in p.threads:
                    for i in t.instructions:
                        if i.state == INITIALISATION:
                            self.execute_instruction(i, t)

    def execute_instruction(self, instruction, t):
        """
        Execute the instruction and update its state
        :param instruction: Instruction that will be executed
        :param t: Thread that executes the instruction
        :return:
        """
        t.state = CHOOSEN
        try:
            instruction.state = IN_EXECUTION
            instruction.exec()
            instruction.state = COMPLETED
            tables = generate_table(self.list_process)
            print_tables(tables)
        except IndexError:
            pass
        t.state = COMPLETED if Thread.check_if_thread_completed(t) else BLOCKED


class Process:
    """
    A class to represent a Process
    """
    process_list = []

    def __init__(self, name, priority, nb_instructions_calcul, nb_instructions_in_out, nb_cycle_before_init, nb_thread):
        """
        Constructs all the necessary attributes for the process object.
        :param name: name of the process
        :param priority: Priority of the process(Threads in the process)
        :param nb_instructions_calcul: Number of the calculation instructions
        :param nb_instructions_in_out: Number of input/output instructions
        :param nb_cycle_before_init: Number of cycle before init
        :param nb_thread: Number of threads in the process
        """
        self.name = name
        self.priority = priority
        self.nb_instructions_calcul = nb_instructions_calcul
        self.nb_instructions_in_out = nb_instructions_in_out
        self.nb_cycle_before_init = nb_cycle_before_init
        self.nb_thread = nb_thread
        self.threads = []
        self.instructions = []
        self.create_instructions_calcul()
        self.create_instructions_in_out()
        self.create_threads()

    def create_instructions_calcul(self):
        # Build a list of calculation instructions
        for nb in range(0, self.nb_instructions_calcul):
            self.instructions.append(Instruction(CALCUL, EXEC_TIME_CALCUL))

    def create_instructions_in_out(self):
        # Build a list of input/output instructions
        for nb in range(0, self.nb_instructions_in_out):
            self.instructions.append(Instruction(IN_OUT, EXEC_TIME_INANDOUT))

    def create_threads(self):
        # Builds a list of threads by distributing instructions between threads
        instructions = self.split_instructions()
        for nb, instruction in zip(range(0, self.nb_thread), instructions):
            self.threads.append(Thread(self.name, nb, instruction))

    def split_instructions(self):
        # Split the list of instructions in order to distribute them between threads
        return np.array_split(self.instructions, self.nb_thread)

    def __str__(self):
        return f'Name: {self.name}\nPriority: {self.priority}\nNumber calcul instructions: ' \
               f'{self.nb_instructions_calcul}\nNumber In/Out: {self.nb_instructions_in_out}\nNumber Cycle: ' \
               f'{self.nb_cycle_before_init}\nNb Thread: {self.nb_thread}\n'


class Thread:
    """
    A class to represent a thread.
    """
    tid = 0

    def __init__(self, t_name, nb, instructions):
        """
        Constructs all the necessary attributes for the thread object.
        :param t_name: Name of the thread
        :param nb: A number that will be suffixed to the name of the thread. eg: t0, t1
        :param instructions: List of all the instructions in the thread
        """
        self.tid = Thread.tid
        self.name = t_name + str(nb)
        self.state = INITIALISATION
        self.instructions = instructions
        Thread.tid += 1

    def check_if_thread_completed(self):
        """
        :return: True if the execution thread is completed
        """
        instruction_executed = 0
        for i in self.instructions:
            if i.state == COMPLETED:
                instruction_executed += 1
        if instruction_executed == len(self.instructions):
            return True
        return False

    def __str__(self):
        return f'\nPID: {self.tid}\nName: {self.name}\nState: {self.state}\n'


class Instruction:
    """
    A class to represent an instruction
    """
    def __init__(self, name, exec_time):
        """
        Constructs all the necessary attributes for the instruction object.
        :param name:
        :param exec_time:
        """
        self.name = name
        self.state = INITIALISATION
        self.exec_time = exec_time

    def exec(self):
        # Sleep for a time to simulate the execution
        self.state = IN_EXECUTION
        time.sleep(self.exec_time)
        self.state = COMPLETED

    def __str__(self):
        return f'Name: {self.name}\nState: {self.state}\nExec Time: {self.exec_time}'
