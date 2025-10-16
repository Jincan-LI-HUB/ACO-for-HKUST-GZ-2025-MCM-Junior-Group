import time
import random
import math

def build_divisibility_graph(n):
    """构建无向整除图"""
    graph = [[] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if j % i == 0:
                graph[i].append(j)
                graph[j].append(i)
    return graph

def is_valid_chain(chain):
    """验证链是否合法"""
    if not chain or len(chain) < 2:
        return False
    for i in range(len(chain)-1):
        a, b = chain[i], chain[i+1]
        if not (b % a == 0 or a % b == 0):
            return False
    return len(set(chain)) == len(chain)

def display_best_chain(chain, total_sum, algorithm_name=""):
    """显示最佳链的完整信息"""
    if not chain:
        print("❌ 没有找到有效链")
        return
    
    print("\n" + "="*70)
    print(f"🎉 {algorithm_name} - 找到最佳链")
    print("="*70)
    print(f"📊 基本信息:")
    print(f"   总和: {total_sum}")
    print(f"   长度: {len(chain)}")
    print(f"   验证: {'通过' if is_valid_chain(chain) else '失败'}")
    print(f"   达成率: {total_sum/5050*100:.2f}%")
    
    print(f"\n🔢 完整数列 ({len(chain)}个数字):")
    print("-" * 60)
    # 每12个数字一行，更清晰的显示
    for i in range(0, len(chain), 12):
        segment = chain[i:i+12]
        line = "  " + " ".join(f"{num:3d}" for num in segment)
        print(line)
    print("-" * 60)
    
    # 详细分析
    used_set = set(chain)
    unused = [x for x in range(1, 101) if x not in used_set]
    unused_big = [x for x in unused if x > 50]
    
    print(f"\n📈 统计分析:")
    print(f"   使用数字: {len(chain)}个")
    print(f"   未使用数字: {len(unused)}个")
    print(f"   未使用大数(>50): {unused_big}")
    
    # 奖励分配
    alice_reward = sum(chain[i] for i in range(0, len(chain), 2))
    bob_reward = sum(chain[i] for i in range(1, len(chain), 2))
    print(f"\n💰 奖励分配:")
    print(f"   Alice奖励: {alice_reward}")
    print(f"   Bob奖励: {bob_reward}")
    print(f"   总奖励: {alice_reward + bob_reward}")
    
    # 链特征
    big_count = len([x for x in chain if x > 50])
    medium_count = len([x for x in chain if 20 <= x <= 50])
    small_count = len([x for x in chain if x < 20])
    avg_size = total_sum / len(chain)
    
    print(f"\n🔍 链特征:")
    print(f"   大数(>50): {big_count}个")
    print(f"   中数(20-50): {medium_count}个")
    print(f"   小数(<20): {small_count}个")
    print(f"   平均数大小: {avg_size:.1f}")
    print("="*70)

def ant_colony_optimization(n=100, num_ants=200, iterations=1000, time_limit=300, alpha=1, beta=2, evaporation_rate=0.3):
    """蚁群算法实现"""
    graph = build_divisibility_graph(n)
    start_time = time.time()
    
    # 初始化信息素矩阵
    pheromone = [[1.0 for _ in range(n+1)] for _ in range(n+1)]
    
    # 启发式信息矩阵
    heuristic = [[0.0 for _ in range(n+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in graph[i]:
            heuristic[i][j] = j
    
    best_chain = []
    best_sum = 0
    improvement_count = 0
    
    print(f"🐜 蚁群算法开始: {num_ants}只蚂蚁, {iterations}次迭代")
    print("=" * 50)
    
    def construct_ant_solution():
        """一只蚂蚁构建解决方案"""
        start = random.randint(1, n)
        path = [start]
        used = set([start])
        
        while True:
            current = path[-1]
            available_neighbors = [nb for nb in graph[current] if nb not in used]
            
            if not available_neighbors:
                break
                
            probabilities = []
            total = 0.0
            
            for nb in available_neighbors:
                p = (pheromone[current][nb]**alpha) * (heuristic[current][nb] ** beta)
                probabilities.append(p)
                total += p
            
            if total == 0:
                next_node = random.choice(available_neighbors)
            else:
                probabilities = [p/total for p in probabilities]
                next_node = random.choices(available_neighbors, weights=probabilities)[0]
            
            path.append(next_node)
            used.add(next_node)
            
            if len(path) >= min(80, n):
                break
        
        return path
    
    for iteration in range(iterations):
        if time.time() - start_time > time_limit:
            break
            
        ant_solutions = []
        
        for ant in range(num_ants):
            solution = construct_ant_solution()
            solution_sum = sum(solution)
            ant_solutions.append((solution, solution_sum))
            
            if solution_sum > best_sum and is_valid_chain(solution):
                best_sum = solution_sum
                best_chain = solution.copy()
                improvement_count += 1
                elapsed = time.time() - start_time
                print(f"🎯 改进 #{improvement_count}: 迭代{iteration+1}, 蚂蚁{ant+1}")
                print(f"   总和: {best_sum}, 长度: {len(best_chain)}, 时间: {elapsed:.1f}s")
        
        # 信息素蒸发和更新(定义已经挪到def函数里面了)
        for i in range(1, n+1):
            for j in range(1, n+1):
                pheromone[i][j] *= (1 - evaporation_rate)
        
        if best_chain:
            valid_solutions = [(sol, ssum) for sol, ssum in ant_solutions if is_valid_chain(sol)]
            if valid_solutions:
                iteration_best_chain, iteration_best_sum = max(valid_solutions, key=lambda x: x[1])
                deposit_amount = iteration_best_sum / 500.0
                
                for i in range(len(iteration_best_chain) - 1):
                    a = iteration_best_chain[i]
                    b = iteration_best_chain[i + 1]
                    pheromone[a][b] += deposit_amount
                    pheromone[b][a] += deposit_amount
        
        # 信息素范围限制
        min_pheromone, max_pheromone = 0.1, 10.0
        for i in range(1, n+1):
            for j in range(1, n+1):
                pheromone[i][j] = max(min_pheromone, min(max_pheromone, pheromone[i][j]))
        
        if (iteration + 1) % 20 == 0:
            valid_solutions = [ssum for sol, ssum in ant_solutions if is_valid_chain(sol)]
            avg_valid = sum(valid_solutions) / len(valid_solutions) if valid_solutions else 0
            elapsed = time.time() - start_time
            print(f"📊 进度: 迭代{iteration+1}/{iterations}, 平均={avg_valid:.0f}, 最佳={best_sum}")
    
    return best_chain, best_sum

if __name__ == "__main__":
    n = 100
    time_limit = 300  # 5分钟
    
    print("🔍 高级算法搜索最大和整除链")
    print("目标: 找到总和最大的合法数列")
    print("=" * 70)
    
    # 运行蚁群算法
    print("\n🐜 运行蚁群算法...")
    chain_aco, sum_aco = ant_colony_optimization(n, time_limit=time_limit)
    
    # 显示蚁群算法结果
    if chain_aco:
        display_best_chain(chain_aco, sum_aco, "蚁群算法")
    else:
        print("❌ 蚁群算法未找到有效链")
    
    # 可以继续添加遗传算法等其他算法...
    # chain_ga, sum_ga = improved_genetic_algorithm(n, time_limit=time_limit)
    # if chain_ga:
    #     display_best_chain(chain_ga, sum_ga, "遗传算法")
    
    print(f"\n⏰ 搜索完成!")