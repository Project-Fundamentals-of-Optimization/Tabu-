

import random
from queue import PriorityQueue

file_path = "/mnt/c/Users/Admin/Desktop/code python/tabu_and_genetic_bản_đầu/data.txt"

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

#########################################


def optimize_route(route):
    # Tham lam
    optimized_route = ''
    remaining_points = route[:]
    current_point = 0

    while remaining_points:
        next_point = min(remaining_points,
                         key=lambda x: distance_matrix[current_point][x])
        optimized_route += str(next_point) + ' '
        remaining_points.remove(next_point)
        current_point = next_point

    return "0 " + optimized_route.strip() + " 0"


def generate_random_sequence4(n, k):
    k = k - 1

    # Ensure every number from 0 to k exists at least once
    sequence = 3 * list(range(k + 1))

    # Fill the remaining elements with random numbers from 0 to k
    sequence += [random.randint(0, k) for _ in range(n - 3 * (k + 1))]

    # Shuffle the sequence to randomize order
    random.shuffle(sequence)

    return sequence


def generate_random_sequence6(n, k):
    k = k - 1
    # Ensure every number from 0 to k exists at least once
    sequence = 7 * list(range(k + 1))

    # Fill the remaining elements with random numbers from 0 to k
    sequence += [random.randint(0, k) for _ in range(n - 7 * (k + 1))]

    # Shuffle the sequence to randomize order
    random.shuffle(sequence)

    return sequence


def generate_random_sequence1(n, k):
    k = k - 1
    # Ensure every number from 0 to k exists at least once
    sequence = 2 * list(range(k + 1))

    # Fill the remaining elements with random numbers from 0 to k
    sequence += [random.randint(0, k) for _ in range(n - 2 * (k + 1))]

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
        if prop < 0.035:
            state = generate_random_sequence_all(n, k)
        elif prop < 0.4:
            state = generate_random_sequence6(n, k)
        elif prop < 0.8:
            state = generate_random_sequence4(n, k)
        else:
            state = generate_random_sequence1(n, k)
    else:
        if prop < 0.33:
            state = generate_random_sequence_all(n, k)
        else:
            state = generate_random_sequence1(n, k)

    return state


initial_state = gen_state(n)

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
MAX_SIZE = 40
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

    return None


for times in range(16000):
    temp_state = gen_state(n)

    v = (-fitness(temp_state, k), temp_state)
    queue_push(v, top_g, is_added, population)


temp_list = []

while not population.empty():
    item = population.get()
    temp_list.append(item)
 # In từng phần tử

# Đưa lại các phần tử vào PriorityQueue
for item in temp_list:
    population.put(item)

################################################


PROP_LOVE = 0.08


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
    if prop < 0.2:

        for i in range(len(p1)):
            if random.random() < PROP_LOVE:
                new_state.append([p1[i], mutation[i]][random.randint(0, 1)])
            else:
                new_state.append([p1[i], p2[i]][random.randint(0, 1)])
    elif prop < 0.5:

        index = random.randint(1, int(len(p1)/2))
        new_state = p1[:index] + p2[index:]

    elif prop < 0.7:
        # thay đổi 1 phần
        for i in range(len(p1)):
            if random.random() < 0.6:
                new_state.append(p1[i])
                continue

            if random.random() < PROP_LOVE:
                new_state.append([p1[i], mutation[i]][random.randint(0, 1)])
            else:
                new_state.append([p1[i], p2[i]][random.randint(0, 1)])
    elif prop < 0.9:
        for i in range(len(p1)):
            if random.random() < 0.6:
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
for i in range(10000):
    v = make_love(top_g, k, PROP_LOVE)

    queue_push((-fitness(v, k), v), top_g, is_added, population)

#################
for c in range(125):
    population_list_temp = take_out_take_back()
    for i in range(110):
        if n < 7:
            p1 = population_list_temp[random.randint(0,  22)]
            p2 = population_list_temp[random.randint(0, 22)]
            v = make_love([p1, p2], k, PROP_LOVE)
            queue_push((-fitness(v, k), v), [p1, p2], is_added, population)
        else:
            p1 = population_list_temp[random.randint(0,  MAX_SIZE - 1)]
            p2 = population_list_temp[random.randint(0,  MAX_SIZE - 1)]
            v = make_love([p1, p2], k, PROP_LOVE)
            queue_push((-fitness(v, k), v), [p1, p2], is_added, population)

for i in range(300):
    v = make_love(top_g, k, PROP_LOVE)

    queue_push((-fitness(v, k), v), top_g, is_added, population)

#################################
temp_list = []
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

print(score)
