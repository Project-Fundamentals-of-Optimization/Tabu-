import random
import numpy as np
from collections import deque
import sys
import time


# start_time = time.time()

# file_path = "/mnt/c/Users/Admin/Desktop/code python/tabu_and_genetic_bản_đầu/data.txt"

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


def initialize_solution_8(n, k):
    solution = [0 for i in range(k)]
    customers = list(range(1, n + 1))
    random.shuffle(customers)
    n_temp = n
    remain_worker = k
    mark = 0
    worker = 0
    while remain_worker > 1:

        length = random.randint(1, n_temp - remain_worker)
        solution[worker] = customers[mark: mark + length]

        # update
        worker += 1
        n_temp -= length
        remain_worker -= 1
        mark += length

    solution[k-1] = customers[mark:]

    return solution


def initialize_solution(n, k):
    solution = [[] for _ in range(k)]

    customers = list(range(1, n + 1))
    random.shuffle(customers)
    for i in range(k):
        solution[i] = optimize_route(customers[i::k])

    return solution


def initialize_solution_5(n, k):
    solution = [[] for _ in range(k)]

    customers = list(range(1, n + 1))
    for i in range(k):
        solution[i].append(customers[i])

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


def initialize_solution_7_random(n, k):
    solution = [[] for _ in range(k)]
    customers = list(range(1, n + 1))
    remaining_customers = n - (0 * (k-1))
    for i in range(k):

        solution[i].append(customers[i])

    temp_i = 0 * k
    for v in range(remaining_customers):
        random_index = random.randint(0, k - 1)
        solution[random_index].append(customers[temp_i + v - 1])

    return solution


def initialize_solution_4(n, k):
    solution = [
        [157, 106, 86, 118, 163, 55, 59, 144, 64,
            122, 161, 91, 90, 48, 76, 51, 30, 191],
        [23, 183, 145, 186, 2, 139, 137, 25, 195, 170,
            147, 67, 69, 63, 92, 121, 75, 197, 94, 47],
        [87, 103, 101, 66, 131, 158, 138, 79, 193, 42,
            116, 182, 151, 155, 189, 141, 72, 13, 39],
        [190, 117, 68, 199, 152, 180, 33, 185, 156, 149,
            54, 172, 133, 82, 3, 150, 12, 167, 88, 44],
        [8, 52, 10, 56, 29, 198, 136, 6, 77, 107, 84,
            200, 83, 100, 38, 32, 31, 21, 188, 70],
        [160, 53, 35, 1, 124, 135, 142, 22, 95, 49, 174,
            26, 115, 146, 73, 165, 166, 128, 187, 19],
        [80, 15, 176, 173, 18, 130, 119, 110, 85, 7, 60, 41, 71, 20, 181, 61],
        [159, 102, 74, 34, 112, 58, 57, 105, 129, 78, 154,
            43, 168, 65, 98, 46, 108, 99, 93, 127, 132],
        [36, 97, 17, 126, 123, 16, 24, 14, 113, 169, 45, 164, 4, 148,
            194, 134, 177, 27, 62, 162, 179, 109, 153, 184, 178, 89],
        [140, 5, 175, 114, 50, 96, 111, 11, 171, 196,
            125, 81, 9, 120, 37, 28, 192, 40, 104, 143]
    ]

    return solution


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


def optimize_route_B(nodes):
    top_remain = 25
    n = len(nodes)
    nodes = [0]+nodes
    init = sum([d[node] for node in nodes])
    new_distance = [[distance_matrix[nodes[i]][nodes[j]]
                     for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for _ in range(n+1)]
    is_[0] = 1

    paths = [[is_[:], init, [0]]]
    new_paths = []

    que = [None, None]

    def push(p):  # p = [mask,length,path]
        if que[0] == None or que[0][1] > p[1]:
            que[0], que[1] = p, que[0]
        elif que[1] == None or que[1][1] > p[1]:
            que[1] = p
    for iter in range(len(nodes[1:])):
        for mask, old_length, path in paths:
            que = [None, None]
            for i in range(1, n+1):
                if mask[i] == 0:
                    mask[i] = 1
                    push([mask[:], old_length-new_distance[path[-1]][0] +
                         new_distance[path[-1]][i]+new_distance[i][0], (path+[i])[:]])
                    mask[i] = 0
            # print(que)
            if que[0] not in new_paths:
                new_paths.append(que[0])
            if que[1] is not None and que[1] not in new_paths:
                new_paths.append(que[1])
            # new_paths.extend(que)
        new_paths = sorted(new_paths, key=lambda p: p[1], reverse=False)

        def cvt(new_paths):
            return [[_1, _2, [nodes[i] for i in path]] for _1, _2, path in new_paths]
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
    top_remain = 30
    n = len(nodes)
    nodes = [0]+nodes
    init = sum([d[node] for node in nodes])
    new_distance = [[distance_matrix[nodes[i]][nodes[j]]
                     for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for _ in range(n+1)]
    is_[0] = 1

    paths = [[is_[:], init, [0]]]
    new_paths = []

    que = [None, None]

    def push(p):  # p = [mask,length,path]
        if que[0] == None or que[0][1] > p[1]:
            que[0], que[1] = p, que[0]
        elif que[1] == None or que[1][1] > p[1]:
            que[1] = p
    for _ in range(len(nodes[1:])):
        for mask, old_length, path in paths:
            que = [None, None]
            for i in range(1, n+1):
                if mask[i] == 0:
                    mask[i] = 1
                    push([mask[:], old_length+new_distance[path[-1]][i], (path+[i])[:]])
                    mask[i] = 0
            if que[0] not in new_paths:
                new_paths.append(que[0])
            if que[1] is not None and que[1] not in new_paths:
                new_paths.append(que[1])
        new_paths = sorted(new_paths, key=lambda p: p[1], reverse=False)
        paths = new_paths[:top_remain]
        new_paths = []
    new_paths = [[_1, _2+new_distance[path[-1]][0], path]
                 for _1, _2, path in new_paths]
    new_paths = sorted(new_paths, key=lambda p: p[1], reverse=False)
    path = paths[0][-1]
    return [nodes[i] for i in path[1:]]


def optimize_route_C_1(nodes):
    top_remain = 20
    n = len(nodes)
    nodes = [0]+nodes
    init = sum([d[node] for node in nodes])
    new_distance = [[distance_matrix[nodes[i]][nodes[j]]
                     for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for _ in range(n+1)]
    is_[0] = 1

    paths = [[is_[:], init, [0]]]
    new_paths = []

    que = [None, None]

    def push(p):  # p = [mask,length,path]
        if que[0] == None or que[0][1] > p[1]:
            que[0], que[1] = p, que[0]
        elif que[1] == None or que[1][1] > p[1]:
            que[1] = p
    for _ in range(len(nodes[1:])):
        for mask, old_length, path in paths:
            que = [None, None]
            for i in range(1, n+1):
                if mask[i] == 0:
                    mask[i] = 1
                    # push([mask[:],old_length+new_distance[path[-1]][i],(path+[i])[:]])
                    new_paths.append(
                        [mask[:], old_length+new_distance[path[-1]][i], (path+[i])[:]])
                    mask[i] = 0
            # if que[0] not in new_paths:new_paths.append(que[0])
            # if que[1] is not None and que[1] not in new_paths:new_paths.append(que[1])
        new_paths = sorted(new_paths, key=lambda p: p[1], reverse=False)
        paths = new_paths[:top_remain]
        new_paths = []
    new_paths = [[_1, _2+new_distance[path[-1]][0], path]
                 for _1, _2, path in new_paths]
    new_paths = sorted(new_paths, key=lambda p: p[1], reverse=False)
    path = paths[0][-1]
    return [nodes[i] for i in path[1:]]


def optimize_route_D(nodes):
    """
    fore sight k step
    """
    n = len(nodes)
    nodes = [0] + nodes
    new_distance = [[distance_matrix[nodes[i]][nodes[j]]
                     for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for node in nodes]
    is_[0] = 1
    path = [0]

    def foresight(i, is_):
        forestep = 10
        length = new_distance[path[-1]][i]
        is_ = is_[:]
        is_[i] = 1
        cur_node = i
        next_node = -1
        for _ in range(forestep):
            next_node = min([i for i in range(len(nodes))], key=lambda x: 1e9 if is_[
                            x] == 1 else new_distance[cur_node][x])
            is_[next_node] = 1
            length += new_distance[cur_node][next_node]
            cur_node = next_node
            if set(is_) == set([1]):
                return length
        return length

    for iter in range(n):
        next_node = min([i for i in range(len(nodes))], key=lambda x: 1e9 if is_[
                        x] == 1 else foresight(x, is_[:]))
        path.append(next_node)
        is_[next_node] = 1
    path = [nodes[i] for i in path[1:]]

    return path


dc = n/k


def optimize_route_E(nodes):
    import math
    """
    fore sight k step
    combine with 
    top - k
    
    """
    global n

    top_remain = 5
    n = len(nodes)
    nodes = [0] + nodes
    # init = sum([d[node] for node in nodes])
    init = 0
    new_distance = [[distance_matrix[nodes[i]][nodes[j]]
                     for i in range(len(nodes))]for j in range(len(nodes))]
    is_ = [0 for node in nodes]
    is_[0] = 1
    path = [0]

    def foresight(i, is_, old_length):
        global n
        global k
        if n == 200 and k == 10:
            forestep = 20
        else:
            forestep = int(10/max(1, math.log10(dc)))
        length = new_distance[path[-1]][i]
        foresight_length = old_length+new_distance[path[-1]][i]
        # distance_matrix
        foresight_path = [(nodes[path[-1]], old_length),
                          (nodes[i], foresight_length)]
        is_ = is_[:]
        is_[i] = 1
        cur_node = i
        next_node = -1
        for _ in range(forestep):
            next_node = min([i for i in range(len(nodes))], key=lambda x: 1e9 if is_[
                            x] == 1 else new_distance[cur_node][x])
            is_[next_node] = 1
            length += new_distance[cur_node][next_node]
            foresight_length += new_distance[cur_node][next_node]
            cur_node = next_node
            foresight_path.append((nodes[cur_node], foresight_length))
            if set(is_) == set([1]):
                return length + new_distance[cur_node][0]
        return length + (new_distance[cur_node][0] if set(is_) == set([1]) else 0)
    length_and_foresight = 0
    length = 0
    paths = [[is_[:], length_and_foresight, [0], length]]
    new_paths = []

    que = [None, None]

    def push(p):  # p = [mask,length,path]
        if que[0] == None or que[0][1] > p[1]:
            que[0], que[1] = p, que[0]
        elif que[1] == None or que[1][1] > p[1]:
            que[1] = p
    for _ in range(len(nodes[1:])):
        for mask, length_and_foresight, path, old_length in paths:
            que = [None, None]
            for i in range(1, n+1):
                if mask[i] == 0:
                    mask[i] = 1
                    push([mask[:], old_length+foresight(i, mask[:], old_length),
                         (path+[i])[:], old_length+new_distance[path[-1]][i]])
                    mask[i] = 0
            # print("U"*30)
            # print(que)
            if que[0] not in new_paths:
                new_paths.append(que[0])
            if que[1] is not None and que[1] not in new_paths:
                new_paths.append(que[1])
        new_paths = sorted(new_paths, key=lambda p: p[1], reverse=False)
        paths = new_paths[:top_remain]
        # print("I"*20)
        paths_cvt = [[_1, _2, [nodes[i] for i in path], _3]
                     for _1, _2, path, _3 in paths]
        # print(paths_cvt)
        new_paths = []
    new_paths = [[_1, _2+new_distance[path[-1]][0], path, _3]
                 for _1, _2, path, _3 in new_paths]
    new_paths = sorted(new_paths, key=lambda p: p[1], reverse=False)
    path = paths[0][-2]

    # print("uncvt",path)
    return [nodes[i] for i in path[1:]]


cnt = 0
sumssss = 0
improvement = 0


def optimize_route(nodes):
    global cnt, sumssss, improvement
    sumssss += 1
    pathA = optimize_route_A(nodes)
    costA = calculate_route_time(pathA)
    pathB = optimize_route_E(nodes)
    costB = calculate_route_time(pathB)
    improvement += costB - costA
    if costA < costB:
        return pathA
    cnt += 1
    return pathB


def calculate_total_time(solution):
    times = [calculate_route_time(route)
             for route in solution]
    return times

################################

# chuẩn hóa dạng


def canonical_form(solution):
    # Sắp xếp các route theo một tiêu chí bất kỳ. Ở đây: dựa trên điểm đầu tiên (nếu route rỗng thì đặt giá trị -1)
    sorted_routes = sorted(
        solution, key=lambda route: route[0] if len(route) > 0 else -1)
    # Chuyển mỗi route thành tuple (immutable) để có thể băm (hash)
    canonical_solution = tuple(tuple(r) for r in sorted_routes)
    return canonical_solution


def tabu_search(solution, max_iter=100):
    # Thay vì chỉ dùng deque, ta dùng thêm set để kiểm tra nhanh
    tabu_list = deque()
    tabu_set = set()

    best_solution = [route[:] for route in solution]
    best_times = calculate_total_time(best_solution)
    best_times_val = max(best_times)
    length_tabu = 0
    for iteration in range(max_iter):
        prop = random.random()
        times = calculate_total_time(solution)
        sorted_times = sorted(
            enumerate(times), key=lambda x: x[1], reverse=True)
        #################################
        if prop < 0.3:
            max_idx, min_idx = sorted_times[0][0], sorted_times[-1][0]
            temp_mem_min = solution[min_idx][:]
            temp_mem_max = solution[max_idx][:]

            temp_length = len(solution[max_idx])
            if temp_length >= 1:
                vertex = random.randint(0, temp_length - 1)
                transfer_point = solution[max_idx][vertex]

                solution[max_idx].remove(transfer_point)
                solution[min_idx].append(transfer_point)

                # Tối ưu lại lộ trình sau khi chuyển giao
                solution[max_idx] = optimize_route(solution[max_idx])
                solution[min_idx] = optimize_route(solution[min_idx])

                # Chuẩn hóa lời giải hiện tại
                canonical_solution = canonical_form(solution)
                if canonical_solution in tabu_set:
                    # Hoàn nguyên nếu muốn, ở đây có thể bỏ qua move
                    # Hoàn nguyên
                    solution[min_idx] = temp_mem_min
                    solution[max_idx] = temp_mem_max
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
            if length_tabu >= 1000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1
        elif prop < 0.4 and k > 7:
            max_idx, min_idx = sorted_times[random.randint(
                0, int(k/4))][0], sorted_times[random.randint(int(k/1.5) + 1, k-1)][0]
            temp_length_max = len(solution[max_idx])
            temp_length_min = len(solution[min_idx])
            if temp_length_max >= 1:
                # Sao lưu trạng thái ban đầu
                temp_mem_max = solution[max_idx][:]
                temp_mem_min = solution[min_idx][:]

                # Tính delta
                delta = int((temp_length_max - temp_length_min - 3)/2)

                # Kiểm tra delta hợp lệ
                if delta > 0 and delta <= temp_length_max:
                    # Chọn các điểm để chuyển từ đầu của max_idx
                    # Những điểm sẽ chuyển
                    multi_transfer_point = temp_mem_max[:delta]
                    # Phần còn lại ở max_idx sau move
                    remaining_max = temp_mem_max[delta:]

                    # Cập nhật lại solution
                    # max_idx giữ lại phần remaining_max
                    solution[max_idx] = remaining_max
                    # min_idx nhận thêm multi_transfer_point
                    solution[min_idx] = temp_mem_min + multi_transfer_point

                    # Tối ưu lại lộ trình sau khi chuyển giao
                    solution[max_idx] = optimize_route(solution[max_idx])
                    solution[min_idx] = optimize_route(solution[min_idx])

                    # Chuẩn hóa lời giải hiện tại
                    canonical_solution = canonical_form(solution)
                    if canonical_solution in tabu_set:
                        # Hoàn nguyên nếu lời giải này đã trong tabu
                        solution[min_idx] = temp_mem_min
                        solution[max_idx] = temp_mem_max
                        continue
                else:
                    # delta không hợp lệ, bỏ qua move này
                    pass

            # Sau khi kết thúc move, đánh giá lại lời giải
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
            if length_tabu >= 1000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1
        elif prop < 0.6 and k > 7:
            max_idx, min_idx = sorted_times[0][0], sorted_times[-1][0]
            temp_length_max = len(solution[max_idx])
            temp_length_min = len(solution[min_idx])
            if temp_length_max >= 1:
                # Sao lưu trạng thái ban đầu
                temp_mem_max = solution[max_idx][:]
                temp_mem_min = solution[min_idx][:]

                # Tính delta
                delta = int((temp_length_max - temp_length_min - 2)/2)

                # Kiểm tra delta hợp lệ
                if delta > 0 and delta <= temp_length_max:
                    # Chọn các điểm để chuyển từ đầu của max_idx
                    # Những điểm sẽ chuyển
                    multi_transfer_point = temp_mem_max[:delta]
                    # Phần còn lại ở max_idx sau move
                    remaining_max = temp_mem_max[delta:]

                    # Cập nhật lại solution
                    # max_idx giữ lại phần remaining_max
                    solution[max_idx] = remaining_max
                    # min_idx nhận thêm multi_transfer_point
                    solution[min_idx] = temp_mem_min + multi_transfer_point

                    # Tối ưu lại lộ trình sau khi chuyển giao
                    solution[max_idx] = optimize_route(solution[max_idx])
                    solution[min_idx] = optimize_route(solution[min_idx])

                    # Chuẩn hóa lời giải hiện tại
                    canonical_solution = canonical_form(solution)
                    if canonical_solution in tabu_set:
                        # Hoàn nguyên nếu lời giải này đã trong tabu
                        solution[min_idx] = temp_mem_min
                        solution[max_idx] = temp_mem_max
                        continue
                else:
                    # delta không hợp lệ, bỏ qua move này
                    pass

            # Sau khi kết thúc move, đánh giá lại lời giải
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
            if length_tabu >= 1000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1
        elif prop < 0.8 and k > 7:
            max_idx, min_idx = sorted_times[0][0], sorted_times[-1][0]
            temp_length_max = len(solution[max_idx])

            find_max_cost = []

            for i in range(temp_length_max):
                if i == 0:
                    find_max_cost.append(
                        distance_matrix[0][solution[max_idx][i]] + distance_matrix[solution[max_idx][i]][solution[max_idx][i+1]])
                elif i == temp_length_max - 1:
                    find_max_cost.append(
                        distance_matrix[solution[max_idx][i-1]][solution[max_idx][i]] + distance_matrix[solution[max_idx][i]][0])

            idx = find_max_cost.index(max(find_max_cost))

            if temp_length_max >= 1:
                vertex = idx
                transfer_point = solution[max_idx][vertex]
                temp_mem_min = solution[min_idx][:]
                temp_mem_max = solution[max_idx][:]
                solution[max_idx].remove(transfer_point)
                solution[min_idx].append(transfer_point)

                # Tối ưu lại lộ trình sau khi chuyển giao
                solution[max_idx] = optimize_route(solution[max_idx])
                solution[min_idx] = optimize_route(solution[min_idx])

                # Chuẩn hóa lời giải hiện tại
                canonical_solution = canonical_form(solution)
                if canonical_solution in tabu_set:
                    # Hoàn nguyên nếu muốn, ở đây có thể bỏ qua move
                    # Hoàn nguyên
                    solution[min_idx] = temp_mem_min
                    solution[max_idx] = temp_mem_max
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
            if length_tabu >= 1000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1
        elif k > 7:
            max_idx, min_idx = sorted_times[0][0], sorted_times[-1][0]
            temp_length_max = len(solution[max_idx])
            temp_length_min = len(solution[min_idx])
            find_max_cost = []
            find_min_cost = []
            for i in range(temp_length_max):
                if i == 0:
                    find_max_cost.append(
                        distance_matrix[0][solution[max_idx][i]] + distance_matrix[solution[max_idx][i]][solution[max_idx][i+1]])
                elif i == temp_length_max - 1:
                    find_max_cost.append(
                        distance_matrix[solution[max_idx][i-1]][solution[max_idx][i]] + distance_matrix[solution[max_idx][i]][0])

            for i in range(temp_length_min):
                if i == 0:
                    find_min_cost.append(
                        distance_matrix[0][solution[max_idx][i]] + distance_matrix[solution[max_idx][i]][solution[max_idx][i+1]])
                elif i == temp_length_max - 1:
                    find_min_cost.append(
                        distance_matrix[solution[max_idx][i-1]][solution[max_idx][i]] + distance_matrix[solution[max_idx][i]][0])
            i

            idx_max_p = find_max_cost.index(max(find_max_cost))
            idx_min_p = find_min_cost.index(min(find_min_cost))
            if temp_length_max >= 1:
                vertex_m = idx_max_p
                transfer_point_max = solution[max_idx][vertex_m]
                transfer_point_min = solution[min_idx][idx_min_p]
                temp_mem_min = solution[min_idx][:]
                temp_mem_max = solution[max_idx][:]
                solution[max_idx].remove(transfer_point_max)
                solution[max_idx].append(transfer_point_min)
                solution[min_idx].append(transfer_point_max)
                solution[min_idx].remove(transfer_point_min)

                # Tối ưu lại lộ trình sau khi chuyển giao
                solution[max_idx] = optimize_route(solution[max_idx])
                solution[min_idx] = optimize_route(solution[min_idx])

                # Chuẩn hóa lời giải hiện tại
                canonical_solution = canonical_form(solution)
                if canonical_solution in tabu_set:
                    # Hoàn nguyên nếu muốn, ở đây có thể bỏ qua move
                    # Hoàn nguyên
                    solution[min_idx] = temp_mem_min
                    solution[max_idx] = temp_mem_max
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
            if length_tabu >= 1000:
                oldest = tabu_list.popleft()
                tabu_set.remove(oldest)
                length_tabu -= 1

    return best_solution, best_times


# print(max(calculate_total_time(initial_solution)))
if k > 7:
    initial_solution = initialize_solution_8(n, k)
    optimized_solution, optimized_times = tabu_search(initial_solution, 4000)
else:
    initial_solution = initialize_solution_3_random(n, k)
    optimized_solution, optimized_times = tabu_search(initial_solution)


print(k)
for sol in optimized_solution:
    print(len(sol)+2)
    print(*([0]+sol+[0]))
print(max(optimized_times))
