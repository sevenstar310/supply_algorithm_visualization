import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy

# 供給処理ロジック
def algorithm(S, D, i, j):
    if S[i]['p'] <= D[j]['p'] or D[j]['p'] >= D[j]['tp']:
        return False
    p_balance = (S[i]['p'] * S[i]['c'] + D[j]['p'] * D[j]['c']) / (S[i]['c'] + D[j]['c'])
    if p_balance < D[j]['tp']:
        S[i]['p'], D[j]['p'] = p_balance, p_balance
        return True
    else:
        S[i]['p'] = (S[i]['p'] * S[i]['c'] + D[j]['p'] * D[j]['c'] - D[j]['tp'] * D[j]['c']) / S[i]['c']
        D[j]['p'] = D[j]['tp']
        return True
    

# メモのアルゴリズム
def sort_algorithm1(S, D):
    S_copy = copy.deepcopy(S)
    D_copy = copy.deepcopy(D)
    S_sorted = sorted(S_copy, key=lambda x: x['p'])  # 供給ボンベ: 初期圧で昇順
    D_sorted = sorted(D_copy, key=lambda x: x['tp'], reverse=True)  # 需要ボンベ: 目標圧で降順
    return S_sorted, D_sorted


# 新しい方のアルゴリズム
def sort_algorithm2(S, D):
    S_copy = copy.deepcopy(S)
    D_copy = copy.deepcopy(D)
    S_sorted = sorted(S_copy, key=lambda x: x['p'])  # 供給ボンベ: 初期圧で昇順
    D_sorted = sorted(D_copy, key=lambda x: x['p'], reverse=True)  # 需要ボンベ: 目標圧で降順
    return S_sorted, D_sorted


def if_feasible(D, ESP):
    res = True
    for d in D:
        if d['p'] < d['tp'] - ESP:
            res = False
            break
    return res


#random.seed(6)

random.seed(9997)
ESP = 1e-7

m = 20  # 供給ボンベ数
n = 10   # 需要ボンベ数
S = [{'i': i, 'c': random.uniform(0, 1), 'p': random.uniform(0, 1)} for i in range(m)]
D = [{'j': j, 'c': random.uniform(0, 1), 'p': random.uniform(0, 0.5), 'tp': random.uniform(0.5, 0.9)} for j in range(n)]


"""*****************************[ アルゴリズムはここを変更する ]*************************************"""
# メモのアルゴリズム ( 需要ボンベ: 目標圧の降順 )
S, D = sort_algorithm1(S, D)

# 新しいアルゴリズム ( 需要ボンベ: 初期圧の降順 )
#S, D = sort_algorithm2(S, D)
"""*****************************[ アルゴリズムはここを変更する ]*************************************"""

for i in range(0, len(S)):
    S[i]["i"] = i
for j in range(0, len(D)):
    D[j]["j"] = j

# アニメーション準備
fig, ax = plt.subplots(figsize=(15, 10))
supply_bars = ax.bar(range(len(S)), [s['p'] for s in S], color='blue', alpha=0.7, label='Supply Tanks')
demand_bars = ax.bar(range(len(S), len(S) + len(D)), [d['p'] for d in D], color='orange', alpha=0.7, label='Demand Tanks')

# 供給ボンベの初期圧を追加
for i, s in enumerate(S):
    ax.hlines(s['p'], i - 0.4, i + 0.4, colors='blue', linestyles='dashed', linewidth=1)
    ax.text(i, s['p'] + 0.03, f"{s['p']:.2f}", color='blue', ha="center", va="bottom", fontsize=8)


# 需要ボンベの目標圧を追加
for i, d in enumerate(D):
    ax.text(len(S) + i, d['tp'], f"{d['tp']:.2f}", color="orange", ha="center", va="bottom", fontsize=8)
    ax.hlines(d['tp'], len(S) + i - 0.4, len(S) + i + 0.4, colors='orange', linestyles='dashed', linewidth=1)

ax.axhline(y=1, color='red', linestyle='--', linewidth=0.8, label='Max Pressure')
ax.set_xticks([])
ax.set_ylim(0, 1.2)
ax.set_ylabel('Pressure')
ax.set_title("Tank Pressure Distribution")
ax.legend()

# アニメーション関数
def animate(frame):
    i = frame // len(D)  # 供給ボンベのインデックス
    j = frame % len(D)   # 需要ボンベのインデックス
    
    if algorithm(S, D, i, j):
        for bar, s in zip(supply_bars, S):
            bar.set_height(s['p'])
        for bar, d in zip(demand_bars, D):
            bar.set_height(d['p'])

ani = animation.FuncAnimation(fig, animate, frames=m * n, interval=100, repeat=True)
plt.show()

    