import random
import time

import numpy as np

import utils  # Custom utility functions package

# Number of ants is 2/3 of the number of cities
num_ant = 4    # Number of ants
alpha = 2  # Pheromone influence factor, values between [1, 5] are suitable
beta = 1  # Expectation influence factor, values between [1, 5] are suitable
info = 0.3  # Pheromone evaporation rate, 0.3 is suitable
Q = 5  # Pheromone increase intensity coefficient

inf = 1e8  # Define infinity value

def cal_newpath(dis_mat, path_new, cityNum):
    """
    Calculate the distances for all paths
    :param dis_mat: Distance matrix ndarray
    :param path_new: Path matrix ndarray
    :param cityNum: Number of cities int
    :return: Optimal path list
    """
    dis_list = []
    for each in path_new:
        dis = 0
        for j in range(cityNum - 1):
            dis = dis_mat[each[j]][each[j + 1]] + dis
        dis = dis_mat[each[cityNum - 1]][each[0]] + dis  # Return home
        dis_list.append(dis)
    return dis_list

def getDisAndPath(point, cityNum, setting):
    """
    Calculate the distances for all paths
    :param point: Distance matrix ndarray
    :param cityNum: Number of cities int
    :param setting: Function related configuration obj, see antColonyOptimization's setting
    :return: Shortest distance double, shortest path list
    """
    dis_mat = np.array(point)  # Convert to matrix
    # Expectation matrix
    e_mat_init = 1.0 / (dis_mat + np.diag([10000] * cityNum))  # Adding diagonal matrix because the divisor cannot be 0
    diag = np.diag([1.0 / 10000] * cityNum)
    e_mat = e_mat_init - diag  # Make diagonal elements 0
    pheromone_mat = np.ones((cityNum, cityNum))  # Initialize pheromone concentration on each edge, all 1 matrix
    path_mat = np.zeros((num_ant, cityNum)).astype(int)  # Initialize paths for each ant, all starting from city 0
    count_iter = 0
    # A counter is set to count consecutive times without better solutions.
    # If the solution in the current iteration is the same as the previous one, the counter increases by 1.
    # When the counter exceeds a threshold, the iteration count is reduced by skipNum, and the counter is reset.
    counter = 0  # Counter for simple optimization of ant colony iterations
    ifOptimanation = setting["ifOptimanation"]
    threshold = setting["threshold"]
    iter_max = setting["iter_max"]
    skipNum = setting["skipNum"]
    pre_min_path = 0
    while count_iter < iter_max:
        for ant in range(num_ant):
            visit = 0  # All starting from city 0
            unvisit_list = list(range(1, cityNum))  # Unvisited cities
            for j in range(1, cityNum):
                # Roulette wheel selection for the next city
                trans_list = []
                tran_sum = 0
                trans = 0
                for k in range(len(unvisit_list)):
                    trans += np.power(pheromone_mat[visit][unvisit_list[k]], alpha) * np.power(
                        e_mat[visit][unvisit_list[k]], beta)
                    trans_list.append(trans)
                    tran_sum = trans
                rand = random.uniform(0, tran_sum)  # Generate random number
                for t in range(len(trans_list)):
                    if rand <= trans_list[t]:
                        visit_next = unvisit_list[t]
                        break
                    else:
                        continue
                path_mat[ant, j] = visit_next  # Fill path matrix
                unvisit_list.remove(visit_next)  # Update
                visit = visit_next  # Update
        # After filling all ants' path tables, calculate the total distance for each ant
        dis_allant_list = cal_newpath(dis_mat, path_mat, cityNum)
        # Update shortest distance and shortest path in each iteration
        if count_iter == 0:
            dis_new = min(dis_allant_list)
            path_new = path_mat[dis_allant_list.index(dis_new)].copy()
        else:
            if min(dis_allant_list) < dis_new:
                dis_new = min(dis_allant_list)
                path_new = path_mat[dis_allant_list.index(dis_new)].copy()
        # Simple optimization for ant colony algorithm iterations
        if ifOptimanation == True:
            if round(pre_min_path, 2) == round(dis_new, 2):
                counter += 1
                if counter >= threshold:
                    iter_max -= skipNum
                    counter = 0
            pre_min_path = dis_new
        # Update pheromone matrix
        pheromone_change = np.zeros((cityNum, cityNum))
        for i in range(num_ant):
            for j in range(cityNum - 1):
                pheromone_change[path_mat[i, j]][path_mat[i, j + 1]] += Q / dis_mat[path_mat[i, j]][path_mat[i, j + 1]]
            pheromone_change[path_mat[i, cityNum - 1]][path_mat[i, 0]] += Q / dis_mat[path_mat[i, cityNum - 1]][
                path_mat[i, 0]]
        pheromone_mat = (1 - info) * pheromone_mat + pheromone_change
        count_iter += 1  # Iteration count +1, enter next iteration
    return dis_new, path_new.tolist(), iter_max

def antColonyOptimization(cityNum, coordinate, point, setting):
    """
    Ant Colony Optimization
    :param cityNum: Number of cities int
    :param coordinate: City coordinates list
    :param point: Distance matrix ndarray
    :param setting: Function related configuration obj
    :return: Minimum distance double, runtime double, number of iterations int

    setting related configuration:
      iter_max: Maximum number of iterations int
      ifOptimanation: Whether to use the optimized scheme bool
      threshold: Threshold int
      skipNum: Number of iterations to skip after reaching the threshold int
    Example:
      setting = {
        "iter_max": 500,
        "ifOptimanation": True,
        "threshold": 6,
        "skipNum": 20
      }
    """
    start = time.perf_counter()  # Program start time
    # skipNum values are 1, 5, 10, 15
    dis, path, iterNum = getDisAndPath(point, cityNum, setting)
    end = time.perf_counter()  # Program end time
    utils.printTable(path, 7, end - start, cityNum, round(dis, 2))  # Print table
    utils.drawNetwork(coordinate, point, path, inf)
    return round(dis, 2), end - start, iterNum
