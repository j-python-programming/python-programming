# Pythonによるプログラミング：第13章　スコープ、実体と参照
# --------------------------
# プログラム名: ex13-deepcopy.py

def deep_copy (x):
    if isinstance(x, list):
        y = []
        for xi in x:
            y.append(deep_copy(xi))
        # リストなら個々に deep_copy したリストを返す
        return y
    else:
        return x  # 値なら、その値を戻す。

x = [[1, 2], [[3, 4, 5], 6, 7], [8, 9, 10]]

y = deep_copy (x)

x [1][0][2] = 100

print ("x = {}".format (x))
print ("y = {}".format (y))
