import numpy as np
import matplotlib.pyplot as plt


def count_islands(grid):
    if not grid.size:
        return 0

    def dfs(row, col):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or grid[row, col] == 0
        ):
            return
        grid[row, col] = 0  # 島を訪れたら0に変更

        # 上下左右の隣接するセルを探索
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    island_count = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 1:
                island_count += 1
                dfs(row, col)  # 島を発見したらDFSで探索

    return island_count


# マップを示すNumPy配列を作成します。0は海、1は島を表します。
pix = 10

grid = np.where(np.random.rand(pix, pix) > 0.95, 1, 0)
grid_ = grid.copy()


island_count = count_islands(grid)
print("島の数:", island_count)
plt.imshow(grid_)
plt.show()
