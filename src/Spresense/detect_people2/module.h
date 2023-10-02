// struct UnionFind
// {
//     // 親の要素とサイズを管理する変数
//     vector<int> parent, size;

//     // 変数の初期化
//     UnionFind(int n) : parent(n, -1), size(n, 1) {}

//     // x の根を求める
//     int root(int x)
//     {
//         // x が根のとき
//         if (parent[x] == -1)
//             return x;

//         // 経路圧縮
//         return parent[x] = root(parent[x]);
//     }

//     // x と y の根が同じか
//     bool isSame(int x, int y)
//     {
//         return root(x) == root(y);
//     }

//     // x と y のグループを併合する
//     void unite(int x, int y)
//     {
//         // x と y の根を取得
//         int rootX = root(x);
//         int rootY = root(y);

//         // x と y が同じグループのときは何もしない
//         if (rootX == rootY)
//             return;

//         // union by size（ y のサイズが小さくなるように調整 ）
//         if (size[rootX] < size[rootY])
//             swap(rootX, rootY);

//         // y の親を x にする
//         parent[rootY] = rootX;

//         // x のサイズに y のサイズを足す
//         size[rootX] += size[rootY];
//     }
// };