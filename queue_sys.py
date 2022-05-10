# Queueing system module

import numpy as np
import pandas as pd

class queue_system:
    def __init__(self):
        self.SERVER1_CAP = 1.5                # The time required for server 1 to complete a stub function
        self.SERVER2_CAP = 1.7                # The time required for server 2 to complete a stub function
        self.NEW_STUB_TIME = 2                # Frequency of generating new stub function (minute)
        self.clock = 0.0                      # simulation clock
        self.num_arrivals = 0                 # total number of arrivals
        self.num_in_q = 0                     # current number in queue
        self.number_in_queue = 0              # total number of stub functions who had to wait in line (counter)
        self.total_wait_time = 0.0            # total wait time
        self.t_arrival = self.gen_int_arr()   # time of next arrival
        self.t_departure1 = float('inf')      # departure time from server 1
        self.t_departure2 = float('inf')      # departure time from server 2
        self.state_T1 = 0                     # current state of server 1 (binary)
        self.state_T2 = 0                     # current state of server 2 (binary)
        self.dep_sum1 = 0                     # Sum of service times by server 1
        self.dep_sum2 = 0                     # Sum of service times by server 2
        self.num_of_departures1 = 0           # number of stub functions processed by server 1  
        self.num_of_departures2 = 0           # number of stub functions processed by server 2 

    def stub_func():
        pass

    def time_adv(self):                                                       
        t_next_event = min(self.t_arrival, self.t_departure1, self.t_departure2)  
        self.total_wait_time += (self.num_in_q * (t_next_event - self.clock))
        self.clock = t_next_event

        if self.t_arrival < self.t_departure1 and self.t_arrival < self.t_departure2:
            self.arrival()
        elif self.t_departure1 < self.t_arrival and self.t_departure1 < self.t_departure2:
            self.server1()
        else:
            self.server2()

    def arrival(self):              
        self.num_arrivals += 1
        self.num_in_system += 1

        # schedule next departure or arrival depending on state of servers
        if self.num_in_q == 0:
            if self.state_T1 == 1 and self.state_T2 == 1:
                self.num_in_q += 1
                self.number_in_queue += 1
                self.t_arrival = self.clock+self.gen_int_arr()
            elif self.state_T1 == 0 and self.state_T2 == 0:
                if np.random.choice([0,1]) == 1:
                    self.state_T1 = 1
                    self.dep1= self.gen_service_time_server1()
                    self.dep_sum1 += self.dep1
                    self.t_departure1 = self.clock + self.dep1
                    self.t_arrival = self.clock+self.gen_int_arr()
                else:
                    self.state_T2 = 1
                    self.dep2 = self.gen_service_time_server2()
                    self.dep_sum2 += self.dep2
                    self.t_departure2 = self.clock + self.dep2
                    self.t_arrival = self.clock + self.gen_int_arr()
            # if server 2 is busy stub function goes to server 1
            elif self.state_T1 == 0 and self.state_T2 == 1:
                self.dep1 = self.gen_service_time_server1()
                self.dep_sum1 += self.dep1
                self.t_departure1 = self.clock + self.dep1
                self.t_arrival = self.clock+self.gen_int_arr()
                self.state_T1 = 1
            # otherwise stub function goes to server 2
            else:
                self.dep2 = self.gen_service_time_server2()
                self.dep_sum2 += self.dep2
                self.t_departure2 = self.clock + self.dep2
                self.t_arrival = self.clock + self.gen_int_arr()
                self.state_T2 = 1
        # if queue length is less than 4 generate next arrival and make stub function join queue
        elif self.num_in_q < 4 and self.num_in_q >= 1:
            self.num_in_q += 1
            self.number_in_queue += 1                             
            self.t_arrival = self.clock + self.gen_int_arr()

    # Server 1 running
    def server1(self):
        self.stub_func()
        self.num_of_departures1 += 1
        if self.num_in_q > 0:
            self.dep1 = self.gen_service_time_server1()
            self.dep_sum1 += self.dep1
            self.t_departure1 = self.clock + self.dep1
            self.num_in_q -= 1
        else:
            self.t_departure1 = float('inf') 
            self.state_T1 = 0                  
    
    # Server 2 running
    def server2(self):
        self.stub_func()
        self.num_of_departures2 += 1
        if self.num_in_q > 0:
            self.dep2 = self.gen_service_time_server2()
            self.dep_sum2 += self.dep2
            self.t_departure2 = self.clock + self.dep2
            self.num_in_q -= 1
        else:
            self.t_departure2 = float('inf')
            self.state_T2 = 0
    
    # function to generate arrival times using inverse trnasform
    def gen_int_arr(self):
        return (-np.log(1-(np.random.uniform(low=0.0, high=1.0))) * self.NEW_STUB_TIME)
    
    # function to generate service time for server 1 using inverse transform
    def gen_service_time_server1(self):
        return (-np.log(1-(np.random.uniform(low=0.0, high=1.0))) * self.SERVER1_CAP)
    
    # function to generate service time for server 1 using inverse transform
    def gen_service_time_server2(self):
        return (-np.log(1-(np.random.uniform(low=0.0, high=1.0))) * self.SERVER2_CAP)

if __name__ == '__main__':
    qs = queue_system()
    df = pd.DataFrame(columns=['Average interarrival time', 'Average service time server 1',
                               'Average service time server 2', 'Utilization server 1', 'Utilization server 2',
                               'Stub function who had to wait in line','Total average wait time'])
    qs.__init__()
    while qs.clock <= 240:
        qs.time_adv() 
    a = pd.Series([qs.clock/qs.num_arrivals, qs.dep_sum1/qs.num_of_departures1,
                   qs.dep_sum2/qs.num_of_departures2, qs.dep_sum1/qs.clock,
                   qs.dep_sum2/qs.clock, qs.number_in_queue, qs.total_wait_time],
                   index=df.columns)
    df = df.append(a,ignore_index=True)

    # Show statistic info
    df.style
