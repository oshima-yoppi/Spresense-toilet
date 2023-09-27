class UnionFind
{
public:
    UnionFind(int n) : N(n)
    {
        for (int i = 0; i < N; i++)
        {
            parent[i] = i;
            rank[i] = 1;
        }
    }

    int find(int x)
    {
        if (x == parent[x])
            return x;
        return parent[x] = find(parent[x]);
    }

    void unite(int x, int y)
    {
        x = find(x);
        y = find(y);

        if (x == y)
            return;

        if (rank[x] < rank[y])
        {
            parent[x] = y;
        }
        else if (rank[x] > rank[y])
        {
            parent[y] = x;
        }
        else
        {
            parent[y] = x;
            rank[x]++;
        }
    }

    int countSets()
    {
        int numSets = 0;

        for (int i = 0; i < N; i++)
        {
            if (find(i) == i)
            {
                numSets++;
            }
        }

        return numSets;
    }

private:
    int N; // 要素の数
    int parent[N];
    int rank[N];
};
