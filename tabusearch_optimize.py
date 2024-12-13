import random
import numpy as np
from collections import deque
import sys
import time


start_time = time.time()

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


###############################################################


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
    route_temp = [0] + route + [0]
    time_val = 0
    for i in range(len(route_temp) - 1):
        time_val += distance_matrix[route_temp[i]][route_temp[i + 1]]
        time_val += d[route_temp[i + 1]]
    return time_val


def optimize_route(route):
    # Tham lam
    optimized_route = []
    remaining_points = route[:]
    current_point = 0

    while remaining_points:
        next_point = min(remaining_points,
                         key=lambda x: distance_matrix[current_point][x])
        optimized_route.append(next_point)
        remaining_points.remove(next_point)
        current_point = next_point

    return optimized_route


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


def tabu_search(solution, max_iter=30000):
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

    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return best_solution, best_times


initial_solution = initialize_solution_2(n, k)
print(initial_solution)
# print(max(calculate_total_time(initial_solution)))
optimized_solution, optimized_times = tabu_search(initial_solution)
print("Total Times:", max(optimized_times))

print("***********************************************")
end_time = time.time()
print(f"Thời gian chạy: {end_time - start_time:.2f} giây")
