import time
import pulp
import Levenshtein

boin = [a for a in "aiueo"]

def name_score(name: str) -> int:
    score = 0
    is_boin = None
    for s in name:
        if (is_boin is not None and (is_boin or (s in boin))):
            score += 1
        is_boin = (s in boin)
    return score / (len(name) - 1)

def target_name(xs, name: str, start: int):
    size = len(name)
    ret = name[start]
    current = start
    for _ in range(size - 1):
        for j in range(size):
            # print("{}({}->{}): {}".format(xs[current][j], name[current], name[j], xs[current][j].value()))
            if xs[current][j].value() == 1:
                ret += name[j]
                current = j
                break
    return ret

def solver(name="sora"):
    original_name = name
    size = len(name)

    # 問題の定義
    prob = pulp.LpProblem('tsp', sense=pulp.LpMaximize)

    # 変数の生成
    xs = []
    for i in range(size):
        x = [pulp.LpVariable('x{}_{}'.format(i, j), cat='Binary') for j in range(size)]
        xs.append(x)
    # 部分順回路排除用
    u = pulp.LpVariable.dicts('u', (i for i in range(size)), lowBound=1, upBound=size, cat='Integer')
    # スタート地点
    x_start = pulp.LpVariable('start', cat='Integer', lowBound=0, upBound=size - 1)

    # スコア生成用の定数配列の生成
    cs = []
    for i in range(size):
        cs.append([])
        for j in range(size):
            if name[i] in boin or name[j] in boin:
                cs[i].append(1)
            else:
                cs[i].append(0)

    # 目的関数
    # TODO: x[?][x_start]は評価に入れない
    prob += pulp.lpSum([pulp.lpDot(c, x) for c, x in zip(cs, xs)]) / size

    # 制約条件
    # 各文字への行きと帰りはそれぞれ一度しか選ばれない
    for i in range(size):
        prob += pulp.lpSum([xs[j][i] for j in range(size)]) == 1
        prob += pulp.lpSum([xs[i][j] for j in range(size)]) == 1

    # おなじ文字には行かない
    for i in range(size):
        prob += xs[i][i] == 0

    # 部分順回路排除用
    # @see: http://www.ie110704.net/2020/08/15/pulp%E3%81%A7%E6%95%B0%E7%90%86%E6%9C%80%E9%81%A9%E5%8C%96%E5%95%8F%E9%A1%8C%EF%BC%88tsp%E3%80%81vrp%EF%BC%89/
    for i in range(size):
        for j in range(size):
            if i != j and (i != 0 and j != 0):
                prob += u[i] - u[j] <= size * (1 - xs[i][j]) - 1

    # スタート地点は文字列の中から選ぶ
    prob += x_start <= size - 1
    prob += 0 <= x_start

    prob.solve()
    print("score:", prob.objective.value())
    print(x_start.value()) # TODO: 制約条件が足りないので最初の文字しか選ばれない
    result = target_name(xs, name, int(x_start.value()))
    return result

if __name__ == '__main__':
    original_name = "sora"

    s = time.time()
    result_name = solver(original_name + "x")
    # result_name = solver(original_name.replace("x", ""))

    # TODO: 先頭が固定になるので、一番いい位置に変える
    s = len(result_name) // 2 - 1
    xname = result_name[s:] + result_name[:s]

    print("time:", time.time() - s)
    print("{}は{}になりました".format(original_name, xname))
    print("name_score({}) = {}".format(xname, name_score(xname)))
