import random
import numpy as np
from collections import deque
import sys
import time

start_time = time.time()

# file_path = "input/input100.txt"

# # Đọc file và xử lý dữ liệu
# with open(file_path, "r") as f:
#     # Đọc dòng 1: chứa N và K
#     first_line = f.readline().strip()
#     n, k = map(int, first_line.split())

#     # Đọc dòng 2: chứa d(1), d(2), ..., d(N)
#     second_line = f.readline().strip()
#     d = [0] + list(map(int, second_line.split()))

#     # Đọc các dòng tiếp theo: ma trận t
#     distance_matrix = []
#     for _ in range(n+1):
#         row = list(map(int, f.readline().strip().split()))
#         distance_matrix.append(row)


# Đọc file và xử lý dữ liệu
    # Đọc dòng 1: chứa N và K
first_line = input()
n, k = map(int, first_line.split())

# Đọc dòng 2: chứa d(1), d(2), ..., d(N)
second_line = input()
d = [0] + list(map(int, second_line.split()))

# Đọc các dòng tiếp theo: ma trận t
distance_matrix = []
for _ in range(n+1):
    row = list(map(int, input().split()))
    distance_matrix.append(row)

###############################################################
# print(cnt)

def initialize_solution(n, k):
    solution = [[] for _ in range(k)]

    customers = list(range(1, n + 1))
    for i in range(k):
        solution[i] = optimize_route(customers[i::k])

    return solution


def initialize_solution_2(n, k):
    solution = [[] for _ in range(k)]
    customers = list(range(1, n + 1))
    random.shuffle(customers)
    chunk_size = n // k  # Kích thước mỗi phần (chia nguyên)
    remainder = n % k  # Số lượng khách hàng dư ra

    start = 0
    for i in range(k):
        end = start + chunk_size

        if remainder > 0:
            end += 1
            remainder -= 1
        solution[i] = customers[start:end]
        start = end

    return solution


def initialize_solution_3_random(n, k):
    solution = [[] for _ in range(k)]
    customers = list(range(1, n + 1))
    remaining_customers = n - (3 * (k-1) + 2)
    for i in range(k):

        solution[i].append(customers[3*i])
        solution[i].append(customers[3*i + 1])
        solution[i].append(customers[3*i + 2])

    temp_i = 3 * k
    for v in range(remaining_customers):
        random_index = random.randint(0, k - 1)
        solution[random_index].append(customers[temp_i + v - 1])

    return solution


def calculate_route_time(route):
    # print("%"*20)
    # print(route)
    route_temp = [0] + route + [0]
    time_val = 0
    
    for i in range(1,len(route_temp)):
        time_val += distance_matrix[route_temp[i-1]][route_temp[i]]
    #     print(f"({time_val},{distance_matrix[route_temp[i-1]][route_temp[i]]} from {route_temp[i-1]} to {route_temp[i]})", end=" ")
    # print()
    for i in range(len(route_temp) - 1):
        time_val += d[route_temp[i + 1]]
    return time_val


def optimize_route_A(route):
    # Tham lam
    optimized_route = [0]
    remaining_points = route[:]
    current_point = 0

    while remaining_points:
        next_point = min(remaining_points,
                         key=lambda x: distance_matrix[current_point][x])
        # print(f"in normal opti",current_point,next_point,distance_matrix[current_point][next_point])
        optimized_route.append(next_point)
        remaining_points.remove(next_point)
        current_point = next_point

    return optimized_route[1:]

def optimize_route_B(nodes):
    top_remain = 30
    n = len(nodes)
    nodes = [0]+nodes
    init = sum([d[node] for node in nodes])
    new_distance = [[distance_matrix[nodes[i]][nodes[j]] for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for _ in range(n+1)]
    is_[0]=1
    
    paths = [[is_[:],init,[0]]]
    new_paths = []
    
    que = [None,None]
    def push(p): #p = [mask,length,path]
        if que[0]==None or que[0][1]>p[1]:
            que[0],que[1] = p,que[0]
        elif que[1]==None or que[1][1]>p[1]:
            que[1]=p
    for iter in range(len(nodes[1:])):
        for mask,old_length,path in paths:
            que = [None,None]
            for i in range(1,n+1):
                if mask[i]==0:
                    mask[i]=1
                    push([mask[:],old_length-new_distance[path[-1]][0]+new_distance[path[-1]][i]+new_distance[i][0],(path+[i])[:]])
                    mask[i]=0
            # print(que)
            if que[0] not in new_paths:new_paths.append(que[0])
            if que[1] is not None and que[1] not in new_paths:new_paths.append(que[1])
            # new_paths.extend(que)
        new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
        def cvt(new_paths):
            return [[_1,_2,[nodes[i] for i in path]] for _1,_2,path in new_paths]
            # for mask,length,path in new_paths:
            #     for node in path:
            #         node = nodes[nodes]
        # print(f"cvt{cvt(new_paths)}")
        paths = new_paths[:top_remain]   
        new_paths = [] 
    path = paths[0][-1]
    # print("siuuuuu",paths[0][1])
    return [nodes[i] for i in path[1:]]

def optimize_route_C(nodes):
    top_remain = 20
    n = len(nodes)
    nodes = [0]+nodes
    init = sum([d[node] for node in nodes])
    new_distance = [[distance_matrix[nodes[i]][nodes[j]] for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for _ in range(n+1)]
    is_[0]=1
    
    paths = [[is_[:],init,[0]]]
    new_paths = []
    
    que = [None,None]
    def push(p): #p = [mask,length,path]
        if que[0]==None or que[0][1]>p[1]:
            que[0],que[1] = p,que[0]
        elif que[1]==None or que[1][1]>p[1]:
            que[1]=p
    for _ in range(len(nodes[1:])):
        for mask,old_length,path in paths:
            que = [None,None]
            for i in range(1,n+1):
                if mask[i]==0:
                    mask[i]=1
                    push([mask[:],old_length+new_distance[path[-1]][i],(path+[i])[:]])
                    mask[i]=0
            if que[0] not in new_paths:new_paths.append(que[0])
            if que[1] is not None and que[1] not in new_paths:new_paths.append(que[1])
        new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
        paths = new_paths[:top_remain]   
        new_paths = [] 
    new_paths = [[_1,_2+new_distance[path[-1]][0],path] for _1,_2,path in new_paths]
    new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
    path = paths[0][-1]
    return [nodes[i] for i in path[1:]]

def optimize_route_C_1(nodes):
    top_remain = 20
    n = len(nodes)
    nodes = [0]+nodes
    init = sum([d[node] for node in nodes])
    new_distance = [[distance_matrix[nodes[i]][nodes[j]] for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for _ in range(n+1)]
    is_[0]=1
    
    paths = [[is_[:],init,[0]]]
    new_paths = []
    
    que = [None,None]
    def push(p): #p = [mask,length,path]
        if que[0]==None or que[0][1]>p[1]:
            que[0],que[1] = p,que[0]
        elif que[1]==None or que[1][1]>p[1]:
            que[1]=p
    for _ in range(len(nodes[1:])):
        for mask,old_length,path in paths:
            que = [None,None]
            for i in range(1,n+1):
                if mask[i]==0:
                    mask[i]=1
                    # push([mask[:],old_length+new_distance[path[-1]][i],(path+[i])[:]])
                    new_paths.append([mask[:],old_length+new_distance[path[-1]][i],(path+[i])[:]])
                    mask[i]=0
            # if que[0] not in new_paths:new_paths.append(que[0])
            # if que[1] is not None and que[1] not in new_paths:new_paths.append(que[1])
        new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
        paths = new_paths[:top_remain]   
        new_paths = [] 
    new_paths = [[_1,_2+new_distance[path[-1]][0],path] for _1,_2,path in new_paths]
    new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
    path = paths[0][-1]
    return [nodes[i] for i in path[1:]]

def optimize_route_D(nodes):
    """
    fore sight k step
    """
    n = len(nodes)
    nodes = [0] + nodes
    new_distance = [[distance_matrix[nodes[i]][nodes[j]] for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for node in nodes]
    is_[0] = 1
    path = [0]

    def foresight(i,is_):
        forestep=10
        length = new_distance[path[-1]][i]
        is_ = is_[:]
        is_[i]=1
        cur_node = i
        next_node = -1
        for _ in range(forestep):
            next_node = min([i for i in range(len(nodes))],key=lambda x: 1e9 if is_[x]==1 else new_distance[cur_node][x])
            is_[next_node] = 1
            length+=new_distance[cur_node][next_node]
            cur_node=next_node
            if set(is_)==set([1]):
                return length
        return length

    for iter in range(n):
        next_node = min([i for i in range(len(nodes))],key=lambda x: 1e9 if is_[x]==1 else foresight(x, is_[:]))
        path.append(next_node)
        is_[next_node]=1
    path = [nodes[i] for i in path[1:]]

    return path

def optimize_route_E(nodes):
    """
    fore sight k step
    combine with 
    top - k
    """
    top_remain = 5
    n = len(nodes)
    nodes = [0] + nodes
    # init = sum([d[node] for node in nodes])
    init=0
    new_distance = [[distance_matrix[nodes[i]][nodes[j]] for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for node in nodes]
    is_[0] = 1
    path = [0]

    def foresight(i,is_,old_length):
        forestep=5
        length = new_distance[path[-1]][i]
        foresight_length = old_length+new_distance[path[-1]][i]
        # distance_matrix
        foresight_path = [(nodes[path[-1]],old_length),(nodes[i],foresight_length)]
        is_ = is_[:]
        is_[i]=1
        cur_node = i
        next_node = -1
        for _ in range(forestep):
            next_node = min([i for i in range(len(nodes))],key=lambda x: 1e9 if is_[x]==1 else new_distance[cur_node][x])
            is_[next_node] = 1
            length+=new_distance[cur_node][next_node]
            foresight_length+=new_distance[cur_node][next_node]
            cur_node=next_node
            foresight_path.append((nodes[cur_node],foresight_length))
            if set(is_)==set([1]):
                # print("#"*40)
                # print(f"try compute foresight from {nodes[path[-1]]} to {nodes[i]}: fore {foresight_path}, real {length}, old {old_length}")
                # print("satisfy the condition")
                return length + new_distance[cur_node][0]
        # print("#"*40)
        # print(f"try compute foresight from {nodes[path[-1]]} to {nodes[i]}: fore {foresight_path}, real {length}, old {old_length}")
        # if set(is_)==set([1]):print("satisfy the condition")
        return length + (new_distance[cur_node][0] if set(is_)==set([1]) else 0)
    length_and_foresight = 0
    length = 0
    paths = [[is_[:],length_and_foresight,[0],length]]
    new_paths = []
    
    que = [None,None]
    def push(p): #p = [mask,length,path]
        if que[0]==None or que[0][1]>p[1]:
            que[0],que[1] = p,que[0]
        elif que[1]==None or que[1][1]>p[1]:
            que[1]=p
    for _ in range(len(nodes[1:])):
        for mask,length_and_foresight ,path, old_length in paths:
            que = [None,None]
            for i in range(1,n+1):
                if mask[i]==0:
                    mask[i]=1
                    push([mask[:],old_length+foresight(i,mask[:],old_length),(path+[i])[:],old_length+new_distance[path[-1]][i]])
                    mask[i]=0
            # print("U"*30)
            # print(que)
            if que[0] not in new_paths:new_paths.append(que[0])
            if que[1] is not None and que[1] not in new_paths:new_paths.append(que[1])
        new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
        paths = new_paths[:top_remain]
        # print("I"*20)
        paths_cvt = [[_1,_2,[nodes[i] for i in path],_3] for _1,_2,path,_3 in paths]
        # print(paths_cvt)   
        new_paths = [] 
    new_paths = [[_1,_2+new_distance[path[-1]][0],path,_3] for _1,_2,path,_3 in new_paths]
    new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
    path = paths[0][-2]
    
    # print("uncvt",path)
    return [nodes[i] for i in path[1:]]
    


# def optimize_route_B(nodes):
#     top_remain = 300
#     top_k = 2
#     # print(nodes)
#     n = len(nodes)
#     nodes = [0]+nodes
#     init = sum([d[node] for node in nodes])
#     new_distance = [[distance_matrix[nodes[i]][nodes[j]] for i in range(len(nodes))]for j in range(len(nodes))]
#     is_ = [0 for _ in range(n+1)]
#     is_[0]=1
    
#     paths = [[is_[:],init,[0]]]
#     new_paths = []
    
#     que = [None,None]
#     def push(p): #p = [mask,length,path]
#         if que[0]==None or que[0][1]>p[1]:
#             que[0],que[1] = p,que[0]
#         elif que[1]==None or que[1][1]>p[1]:
#             que[1]=p
#     for iter in range(len(nodes[1:])):
#         for mask,old_length,path in paths:
#             que = [None,None]
#             for i in range(1,n+1):
#                 if mask[i]==0:
#                     mask[i]=1
#                     push([mask[:],old_length-new_distance[path[-1]][0]+new_distance[path[-1]][i]+new_distance[i][0],(path+[i])[:]])
#                     mask[i]=0
#             # print(que)
#             if que[-1]==None:que=que[:-1]
#             if que[-1]==None:que=que[:-1]
#             new_paths.extend(que)
#         new_paths = sorted(new_paths,key=lambda p:p[1],reverse=False)
#         paths = new_paths[:top_remain]   
#         new_paths = [] 
#     path = paths[0][-1]
#     print("siuuuuu",paths[0][1])
#     return [nodes[i] for i in path[1:]]
cnt=0
sumssss = 0
improvement = 0
def optimize_route(nodes):
    global cnt,sumssss,improvement
    sumssss+=1
    pathA = optimize_route_A(nodes)
    costA = calculate_route_time(pathA)
    pathB = optimize_route_E(nodes)
    costB = calculate_route_time(pathB)
    improvement +=costB - costA
    if costA<costB:
        return pathA
    cnt+=1
    return pathB
    # print(uA:=optimize_route_A(nodes),uA:=calculate_route_time(uA))
    # print("^"*80)
    # print(uB:=optimize_route_E(nodes),uB:=calculate_route_time(uB))
    # if uA<uB: print(f"okkkkkkkkk: uA {uA}, uB {uB}")
    # exit(0)


def calculate_total_time(solution):
    times = [calculate_route_time(route)
             for route in solution]
    return times

################################

# chuẩn hóa dạng
def hash_(solution):
    p1 = 10888869450418352160768000001
    p2 = 3001
    res = 0
    for u in solution:
        for o in u:
            res =( res*p2+o)%p1
        res = (res*p2-p2)%p1
    return res



def canonical_form(solution):
    # Sắp xếp các route theo một tiêu chí bất kỳ. Ở đây: dựa trên điểm đầu tiên (nếu route rỗng thì đặt giá trị -1)
    sorted_routes = sorted(
        solution, key=lambda route: route[0] if len(route) > 0 else -1)
    # Chuyển mỗi route thành tuple (immutable) để có thể băm (hash)
    canonical_solution = tuple(tuple(r) for r in sorted_routes)
    return canonical_solution


def tabu_search(solution, max_iter=10000):
    # Thay vì chỉ dùng deque, ta dùng thêm set để kiểm tra nhanh
    tabu_list = deque()
    tabu_set = set()

    best_solution = [route[:] for route in solution]
    ###############################################
    # optimize_route(best_solution[0])
    ##############################################
    best_times = calculate_total_time(best_solution)
    best_times_val = max(best_times)
    length_tabu = 0
    from time import perf_counter
    for iteration in range(max_iter):
        tin = perf_counter()
        prop = random.random()
        times = calculate_total_time(solution)
        sorted_times = sorted(
            enumerate(times), key=lambda x: x[1], reverse=True)
        #################################
        if prop < 0.8:
            max_idx, min_idx = sorted_times[0][0], sorted_times[-1][0]
            temp_length = len(solution[max_idx])
            if temp_length >= 1:
                vertex = random.randint(0, temp_length - 1)
                transfer_point = solution[max_idx][vertex]

                solution[max_idx].remove(transfer_point)
                solution[min_idx].insert(-1, transfer_point)

                # Tối ưu lại lộ trình sau khi chuyển giao
                solution[max_idx] = optimize_route(solution[max_idx])
                solution[min_idx] = optimize_route(solution[min_idx])

                # Chuẩn hóa lời giải hiện tại
                canonical_solution = canonical_form(solution)
                if canonical_solution in tabu_set:
                    # Hoàn nguyên nếu muốn, ở đây có thể bỏ qua move
                    # Hoàn nguyên
                    solution[min_idx].remove(transfer_point)
                    solution[max_idx].insert(vertex, transfer_point)
                    continue

            times = calculate_total_time(solution)
            if max(times) < best_times_val:
                best_solution = [route[:] for route in solution]
                best_times = times
                best_times_val = max(times)
                # Thêm vào tabu
                canonical_best = canonical_form(best_solution)
                tabu_list.append(canonical_best)
                tabu_set.add(canonical_best)
                length_tabu += 1
            if length_tabu >= 10000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1

        elif prop < 0.9:
            max_idx, min_idx = sorted_times[random.randint(
                2, int(k/2))][0], sorted_times[random.randint(int(k/2) + 1, k-1)][0]

            temp_length = len(solution[max_idx])
            if temp_length >= 1:
                vertex = random.randint(0, temp_length - 1)
                transfer_point = solution[max_idx][vertex]

                solution[max_idx].remove(transfer_point)
                solution[min_idx].insert(-1, transfer_point)

                solution[max_idx] = optimize_route(solution[max_idx])
                solution[min_idx] = optimize_route(solution[min_idx])

                canonical_solution = canonical_form(solution)
                if canonical_solution in tabu_set:
                    # Hoàn nguyên
                    solution[min_idx].remove(transfer_point)
                    solution[max_idx].insert(vertex, transfer_point)
                    continue

            times = calculate_total_time(solution)
            if max(times) < best_times_val:
                best_solution = [route[:] for route in solution]
                best_times = times
                best_times_val = max(times)
                canonical_best = canonical_form(best_solution)
                tabu_list.append(canonical_best)
                tabu_set.add(canonical_best)
                length_tabu += 1
            if length_tabu >= 10000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1

        else:
            max_idx, min_idx = sorted_times[random.randint(
                0,  int(k/2))][0], sorted_times[random.randint(
                    int(k/1.4), k-1)][0]

            temp_length = len(solution[max_idx])
            if temp_length >= 1:
                vertex = random.randint(0, temp_length - 1)
                transfer_point = solution[max_idx][vertex]

                # just swap
                old_val = solution[min_idx][-1]
                solution[max_idx][vertex], solution[min_idx][-1] = old_val, transfer_point

                solution[max_idx] = optimize_route(solution[max_idx])
                solution[min_idx] = optimize_route(solution[min_idx])

                canonical_solution = canonical_form(solution)
                if canonical_solution in tabu_set:
                    # Hoàn nguyên
                    solution[max_idx][vertex], solution[min_idx][-1] = transfer_point, old_val
                    continue

            times = calculate_total_time(solution)
            if max(times) < best_times_val:
                best_solution = [route[:] for route in solution]
                best_times = times
                best_times_val = max(times)
                canonical_best = canonical_form(best_solution)
                tabu_list.append(canonical_best)
                tabu_set.add(canonical_best)
                length_tabu += 1
            if length_tabu >= 10000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1
        # if iteration%500==0:
    #         print(f"epoch {iteration} in {perf_counter()-tin:.4f}s with rate {cnt/sumssss:.2f} and improvement {improvement/sumssss:.2f}")

    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return best_solution, best_times


initial_solution = initialize_solution_2(n, k)
# print(initial_solution)
optimized_solution, optimized_times = tabu_search(initial_solution)
for sol in optimized_solution:
    print(len(sol)+2)
    print(*sol)
# print(max(calculate_total_time(optimized_solution)))

# print("Total Times:", max(optimized_times))

# print("***********************************************")
# end_time = time.time()
# print(f"Thời gian chạy: {end_time - start_time:.2f} giây")
