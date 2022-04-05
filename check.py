import numpy as np

array = np.linspace(1,100,100)
numpoints = 7

n = len(array)/numpoints # number of intervals in my array

if n%1==0:
    print(int(n))

#
# timeperpoint = 0.02 # time per point (s)
# tau_array = np.linspace(0.01, 1, 100) # averaging time (s)
#
# Allan_squared_array = []
# for index_tau in range(len(tau_array)):
#     tau_soln = tau_array[index_tau]
#     numpoints = tau_soln/timeperpoint # number of points in time interval tau
#     M = np.int(len(array)/numpoints) # number of intervals in my array
#     n = 2
#
#     Allan_squared = 0
#     for index_n in range(n-1):
#         #avg_diff_soln = (np.average(array[index_M+1:M+index_M+1])-np.average(array[index_M:M+index_M]))**2
#         index_n = 0
#         avg_diff_soln = array[index_n+1:n+index_n+1]-array[index_n:n+index_n]
#         Allan_squared_soln = (1/2)*avg_diff_soln
#         Allan_squared = Allan_squared + Allan_squared_soln
#
#     Allan_squared_array = np.append(Allan_squared_array,Allan_squared)
