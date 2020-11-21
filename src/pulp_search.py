import time
import pulp
from pprint import pprint

from src.common import vowels, name_score

# 名前順列行列から文字列を復元する
def target_name(xs, name: str):
    size = len(name)
    start = 0
    # 最初の文字を探す
    for j in range(size):
        if (all([xs[i][j] == 0 for i in range(size)])):
            start = j

    # debug
    # for i in range(size):
    #     for j in range(size):
    #         if xs[i][j] == 1:
    #             print("debug: {}({}->{}): {}".format(xs[i][j], name[i], name[j], xs[i][j]))

    ret = name[start]
    current = start
    for _ in range(size - 1):
        for j in range(size):
            if xs[current][j] == 1:
                ret += name[j]
                current = j
                break
    return ret

def solver(name: str):
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

    # スコア生成用の定数配列の生成
    cs = []
    for i in range(size):
        cs.append([])
        for j in range(size):
            if name[i] in vowels or name[j] in vowels:
                cs[i].append(1)
            else:
                cs[i].append(0)

    # 目的関数
    prob += pulp.lpSum([pulp.lpDot(c, x) for c, x in zip(cs, xs)])

    # 制約条件
    # 各文字への行きと帰りはそれぞれ一度しか選ばれない
    for i in range(size):
        prob += pulp.lpSum([xs[j][i] for j in range(size)]) <= 1
        prob += pulp.lpSum([xs[i][j] for j in range(size)]) <= 1
    # n文字(n-1回の連結)
    prob += pulp.lpSum([pulp.lpSum([x2 for x2 in x1]) for x1 in xs]) == size - 1

    # おなじ文字には行かない
    for i in range(size):
        prob += xs[i][i] == 0

    # 部分順回路排除用
    # @see: http://www.ie110704.net/2020/08/15/pulp%E3%81%A7%E6%95%B0%E7%90%86%E6%9C%80%E9%81%A9%E5%8C%96%E5%95%8F%E9%A1%8C%EF%BC%88tsp%E3%80%81vrp%EF%BC%89/
    for i in range(size):
        for j in range(size):
            if i != j: # ハミルトン閉路ではi,j == 0のとき制約を追加しない
                prob += u[i] - u[j] <= (1 - xs[i][j]) * size - 1

    # 行きか帰りに一度は選ばれる
    for i in range(size):
        prob += pulp.lpSum([xs[i][j] for j in range(size)]) + pulp.lpSum([xs[j][i] for j in range(size)]) >= 1

    pulp.PULP_CBC_CMD(msg=0, timeLimit=1, options = ['maxsol 1']).solve(prob)
    xs = [[round(x2.value()) for x2 in x1] for x1 in xs]
    if prob.status != 1: print(prob.status, pulp.LpStatus[prob.status])
    # print("score:", prob.objective.value())
    # pprint(xs)
    # pprint([u1 for u1 in u])
    result = target_name(xs, name)

    return (result, prob.objective.value())

if __name__ == '__main__':
    original_name = input('input name: ') + "x"

    s = time.time()
    xname = solver(original_name)

    print("time:", time.time() - s)
    print("{}は{}になりました".format(original_name, xname))
    print("name_score({}) = {}".format(xname, name_score(xname)))
