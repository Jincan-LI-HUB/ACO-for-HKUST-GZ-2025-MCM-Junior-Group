import time

def build_divisibility_graph(n):
    """构建无向整除图"""
    graph = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if j % i == 0:
                graph[i].append(j)
                graph[j].append(i)
    return graph

def simple_effective_dfs(n=100, time_limit=120):
    """简单但有效的DFS，主要靠搜索顺序优化"""
    graph = build_divisibility_graph(n)
    best_chain = []
    best_sum = 0
    start_time = time.time()
    
    # 预计算：每个数字的"大数邻居"数量（完整的计算）
    big_neighbor_count = [0] * (n+1)
    for i in range(1, n+1):
        big_neighbors = [x for x in graph[i] if x > i and x >= n//2]  # 比自己大且是较大数
        big_neighbor_count[i] = len(big_neighbors)
    
    def dfs(path, used, current_sum):
        nonlocal best_chain, best_sum
        
        if time.time() - start_time > time_limit:
            return True
        
        # 更新最优解
        if current_sum > best_sum:
            best_sum = current_sum
            best_chain = path.copy()
            print(f"新最大和: {best_sum}, 长度: {len(path)}, 时间: {time.time()-start_time:.1f}s")
        
        current = path[-1]
        
        # 关键优化：邻居排序策略
        neighbors = [x for x in graph[current] if x not in used]
        
        # 排序策略：优先大数，但也要考虑连接大数的能力
        neighbors.sort(key=lambda x: (
            x,  # 主要按数字大小
            -big_neighbor_count[x]  # 其次按连接大数的能力（负数因为reverse=True）
        ), reverse=True)
        
        for nb in neighbors:
            used.add(nb)
            path.append(nb)
            
            # 只有一个简单剪枝：如果剩余所有数字都加上也不如当前最佳解
            remaining_max = sum(x for x in range(n, 0, -1) if x not in used)
            if current_sum + nb + remaining_max > best_sum:  # 宽松条件
                if dfs(path, used, current_sum + nb):
                    return True
                    
            path.pop()
            used.remove(nb)
        
        return False
    
    # 从高质量起点开始（基于度数和数字大小）
    good_starts = [96, 100, 99, 98, 97, 95, 94, 92, 90, 88, 84, 80, 78, 72, 64]
    
    for start in good_starts:
        if time.time() - start_time > time_limit:
            break
        print(f"尝试起点: {start}")
        dfs([start], {start}, start)
    
    return best_chain, best_sum

def verify_chain(chain):
    """验证链是否合法"""
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i + 1]
        if not (b % a == 0 or a % b == 0):
            return False
    if len(set(chain)) != len(chain):
        return False
    return True

if __name__ == "__main__":
    n = 100
    print("搜索总和最大的整除链...")
    chain, total = simple_effective_dfs(n, time_limit=120)
    
    print("\n最终结果:")
    print(f"链长度: {len(chain)}")
    print(f"链总和: {total}")
    print(f"验证通过: {verify_chain(chain)}")
    print(f"链: {chain}")
    
    # 输出未使用的大数
    used_set = set(chain)
    unused_big = [x for x in range(100, 0, -1) if x not in used_set]
    print(f"未使用的大数: {unused_big[:20]}")