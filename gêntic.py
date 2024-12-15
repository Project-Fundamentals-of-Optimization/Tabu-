# Đường dẫn tới file
import random
from queue import PriorityQueue
import sys

import time

# Bắt đầu đo thời gian
start_time = time.time()


file_path = "data.txt"

# Đọc file và xử lý dữ liệu
with open(file_path, "r") as f:
    # Đọc dòng 1: chứa N và K
    first_line = f.readline().strip()
    n, k = map(int, first_line.split())

    # Đọc dòng 2: chứa d(1), d(2), ..., d(N)
    second_line = f.readline().strip()
    d = [0] + list(map(int, second_line.split()))

    # Đọc các dòng tiếp theo: ma trận t
    distance_matrix = []
    for _ in range(n+1):
        row = list(map(int, f.readline().strip().split()))
        distance_matrix.append(row)

# """# khởi tạo trạng thái ban đầu"""

# Đọc file và xử lý dữ liệu
    # Đọc dòng 1: chứa N và K
# first_line = input()
# n, k = map(int, first_line.split())

# # Đọc dòng 2: chứa d(1), d(2), ..., d(N)
# second_line = input()
# d = [0] + list(map(int, second_line.split()))

# # Đọc các dòng tiếp theo: ma trận t
# distance_matrix = []
# for _ in range(n+1):
#     row = list(map(int, input().split()))
#     distance_matrix.append(row)


#########################################

def calculate_route_time(route):
    route_temp = [0] + route + [0]
    time_val = 0
    for i in range(len(route_temp) - 1):
        time_val += distance_matrix[route_temp[i]][route_temp[i + 1]]
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

dc = n/k
def optimize_route_E(nodes):
    import math
    """
    fore sight k step
    combine with 
    top - k
    """
    top_remain = 4
    n = len(nodes)
    nodes = [0] + nodes
    # init = sum([d[node] for node in nodes])
    init=0
    new_distance = [[distance_matrix[nodes[i]][nodes[j]] for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for node in nodes]
    is_[0] = 1
    path = [0]

    def foresight(i,is_,old_length):
        forestep=25
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
                return length + new_distance[cur_node][0]
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

def optimize_route(route):
    rA = optimize_route_A(route)
    rC = optimize_route_C(route)
    cA = calculate_route_time(rA)
    cC = calculate_route_time(rC)
    # print(cA,rA)
    # print(cC,rC)
    if cA>cC: route = rC
    else: route = rA
    # print(route)
    route = [0]+route+[0]
    o = " ".join([str(i) for i in route])
    # print(o[:-1])
    # exit(0)
    return o

def generate_random_sequence4(n, k):
    k = k - 1

    # Ensure every number from 0 to k exists at least once
    sequence = 4 * list(range(k + 1))

    # Fill the remaining elements with random numbers from 0 to k
    sequence += [random.randint(0, k) for _ in range(n - 4 * (k + 1))]

    # Shuffle the sequence to randomize order
    random.shuffle(sequence)

    return sequence


def generate_random_sequence6(n, k):
    k = k - 1
    # Ensure every number from 0 to k exists at least once
    sequence = 6 * list(range(k + 1))

    # Fill the remaining elements with random numbers from 0 to k
    sequence += [random.randint(0, k) for _ in range(n - 6 * (k + 1))]

    # Shuffle the sequence to randomize order
    random.shuffle(sequence)

    return sequence


def generate_random_sequence1(n, k):
    k = k - 1
    # Ensure every number from 0 to k exists at least once
    sequence = 1 * list(range(k + 1))

    # Fill the remaining elements with random numbers from 0 to k
    sequence += [random.randint(0, k) for _ in range(n - 1 * (k + 1))]

    # Shuffle the sequence to randomize order
    random.shuffle(sequence)

    return sequence


def generate_random_sequence_all(n, k):
    base_count = n // k
    sequence = [i for i in range(k) for _ in range(base_count)]

    # Số phần tử còn lại cần bổ sung
    remaining = n - len(sequence)

    # Thêm các số ngẫu nhiên từ 0 đến k-1
    random_part = [random.randint(0, k-1) for _ in range(remaining)]
    sequence.extend(random_part)

    # Trộn lại dãy để đảm bảo tính ngẫu nhiên
    random.shuffle(sequence)
    return sequence


def gen_state(n):
    prop = random.random()
    if n > 30:
        if prop < 0.01:
            state = generate_random_sequence_all(n, k)

        elif prop < 0.9:
            state = generate_random_sequence4(n, k)
        else:
            state = generate_random_sequence6(n, k)
    else:
        if prop < 0.1:
            state = generate_random_sequence_all(n, k)
        else:
            state = generate_random_sequence1(n, k)
    return state


###########################################################################
"""## hàm fitness"""


def greedy_search(worker_k, store_path):
    route_of_k = store_path[worker_k]
    start_node = 0
    set_of_nodes = set(route_of_k)
    optimize_path = []
    while set_of_nodes:
        temp = []
        for i in set_of_nodes:
            temp.append((distance_matrix[start_node][i], i))
        start_node = min(temp)[1]
        optimize_path.append(start_node)
        set_of_nodes.remove(start_node)
        continue

    return optimize_path


def fitness(state, K):
    store_path = {}
    for i, k in enumerate(state):
        store_path[k] = store_path.get(k, []) + [i + 1]
    for k in range(K):
        store_path[k] = greedy_search(k, store_path)

    total_distance_of_each_k = [0 for _ in range(K)]

    for worker in range(K):
        pre = 0
        for node in store_path[worker] + [0]:  # [2,4,5,0]

            total_distance_of_each_k[worker] += distance_matrix[pre][node] + d[node]

            pre = node

    return max(total_distance_of_each_k)

# print(initial_state)
# print(fitness(initial_state,k))


"""# khởi tạo các giá trị ban đầu vào population"""

population = PriorityQueue()
MAX_SIZE = 300
top_g = [None, None]  # g<10 push ~ O(1) but g -> 100 slow
is_added = {}


def queue_push(v, top_g, is_added, population):

    if is_added.get(tuple(v[1]), None) != None:
        return None
    elif top_g[0] is None:
        top_g[0] = v
        is_added[tuple(top_g[0][1])] = 1
        population.put(v)
    elif top_g[1] is None:
        if -v[0] < -top_g[0][0]:
            top_g[1] = top_g[0]
            top_g[0] = v
            is_added[tuple(top_g[0][1])] = 1
            population.put(v)
        else:
            top_g[1] = v
            is_added[tuple(top_g[1][1])] = 1
            population.put(v)
    else:
        if -v[0] < -top_g[0][0]:
            top_g[1] = top_g[0]
            top_g[0] = v
            is_added[tuple(top_g[0][1])] = 1
            population.put(v)
        elif -v[0] < -top_g[1][0]:
            top_g[1] = v
            is_added[tuple(top_g[1][1])] = 1
            population.put(v)
        else:
            is_added[tuple(v[1])] = 1
            population.put(v)

    if population.qsize() > MAX_SIZE:
        return population.get()
        print("pop")  # get = pop
    return None


for times in range(15000):
    temp_state = gen_state(n)

    v = (-fitness(temp_state, k), temp_state)
    queue_push(v, top_g, is_added, population)


# temp_list = []

# while not population.empty():
#     item = population.get()
#     temp_list.append(item)
#  # In từng phần tử

# # Đưa lại các phần tử vào PriorityQueue
# for item in temp_list:
#     population.put(item)

################################################


PROP_LOVE = 0.03


def check_legit_childe(state, K):
    for i in range(K):
        if i not in state:
            return False
    return True


def take_out_take_back():
    temp_list = []

    while not population.empty():

        item = population.get()

        temp_list.append(item)
    # Đưa lại các phần tử vào PriorityQueue
    for item in temp_list:
        population.put(item)

    return temp_list
#############################################


def make_love(top_g, K, PROP_LOVE):
    prop = random.random()
    new_state = []
    # unpack top_g -> parents
    p1, p2 = top_g
    _, p1 = p1
    _, p2 = p2
    # make_love
    mutation = gen_state(n)
    if prop < 0.3:

        for i in range(len(p1)):
            if random.random() < PROP_LOVE:
                new_state.append([p1[i], mutation[i]][random.randint(0, 1)])
            else:
                new_state.append([p1[i], p2[i]][random.randint(0, 1)])
    elif prop < 0.7:
        vl_temp = len(p1)
        index = random.randint(int(vl_temp/4), int(vl_temp/1.5))
        new_state = p1[:index] + p2[index:]

    elif prop < 0.8:
        # thay đổi 1 phần
        for i in range(len(p1)):
            if random.random() < 0.5:
                new_state.append(p1[i])
                continue

            if random.random() < PROP_LOVE:
                new_state.append([p1[i], mutation[i]][random.randint(0, 1)])
            else:
                new_state.append([p1[i], p2[i]][random.randint(0, 1)])
    elif prop < 0.9:
        for i in range(len(p1)):
            if random.random() < 0.5:
                new_state.append(p2[i])
                continue

            if random.random() < PROP_LOVE:
                new_state.append([p1[i], mutation[i]][random.randint(0, 1)])
            else:
                new_state.append([p1[i], p2[i]][random.randint(0, 1)])
    elif prop < 0.95:
        for i in range(len(p1)):
            if i % 2 == 0:
                new_state.append(p2[i])
                continue
            else:
                new_state.append(p1[i])
                continue
    else:
        for i in range(len(p1)):
            if i % 2 == 0:
                new_state.append(p1[i])
                continue
            else:
                new_state.append(p2[i])
                continue

    # avoid 1 worker carry all
    if check_legit_childe(new_state, K):
        return new_state
    else:
        return make_love(top_g, K, PROP_LOVE)


###################################################################################################
for i in range(5000):
    v = make_love(top_g, k, PROP_LOVE)

    queue_push((-fitness(v, k), v), top_g, is_added, population)


#################
for c in range(150):
    population_list_temp = take_out_take_back()
    for i in range(300):
        p1 = population_list_temp[random.randint(0,  MAX_SIZE-1)]
        p2 = population_list_temp[random.randint(0, MAX_SIZE-1)]
        v = make_love([p1, p2], k, PROP_LOVE)
        queue_push((-fitness(v, k), v), [p1, p2], is_added, population)


#################################
temp_list = []

i = 1
while not population.empty():

    item = population.get()

    temp_list.append(item)

# Đưa lại các phần tử vào PriorityQueue
best = item[1]
score = item[0]
for item in temp_list:
    population.put(item)

#################################
# output
print(k)
for worker in range(k):
    temp = []

    for index in range(n):
        if best[index] == worker:
            temp.append(index + 1)

    print(len(temp) + 2)
    print(optimize_route(temp))


print("***********************************************")
# Kết thúc đo thời gian
end_time = time.time()

# In thời gian chạy
print(f"Thời gian chạy: {end_time - start_time:.2f} giây")
print("score" + str(-score))

