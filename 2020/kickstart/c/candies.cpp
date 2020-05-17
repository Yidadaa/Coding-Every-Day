#include <iostream>

using namespace std;

class Node
{
public:
    int l = 0, r = 0;
    Node* lchild = nullptr;
    Node* rchild = nullptr;
    int val = 0, sweet = 0;
    bool empty = true;

    Node(int l, int r)
    {
        this->l = l;
        this->r = r;
        empty = false;
    }

    Node() {}
};

class Tree
{
public:
    int nums[100005];
    int n = 0;
    Node* tree;
    Node* q[100005];

    Tree(int nums[], int n)
    {
        for (int i = 0; i < n; i += 1) this->nums[i] = nums[i];
        tree = build(0, n - 1);
    }

    ~Tree()
    {
        for (int i = 0; i < n; i += 1) delete tree;
    }

    Node* build(int l, int r)
    {
        if (l > r) return nullptr;
        Node* node = new Node(l, r);
        if (l == r)
        {
            node->sweet = nums[l] * (l + 1) * (l % 2 ? -1 : 1);
            node->val = nums[l] * (l % 2 ? -1 : 1);
            return node;
        }
        int m = (l + r) >> 1;
        node->lchild = build(l, m);
        node->rchild = build(m + 1, r);
        node->sweet = node->lchild->sweet + node->rchild->sweet;
        node->val = node->lchild->val + node->rchild->val;
        return node;
    }

    void update(int i, int val)
    {
        i -= 1;
        int d = val - nums[i];
        nums[i] = val;
        q[0] = tree;
        int count = 1;
        while (count)
        {
            Node* node = q[count - 1];
            count -= 1;
            if (i >= node->l && i <= node->r)
            {
                node->val += d * (i % 2 ? -1 : 1);
                node->sweet += d * (i + 1) * (i % 2 ? -1 : 1);
            } else continue;
            if (!node->lchild->empty)
            {
                q[count] = node->lchild;
                count += 1;
            }
            if (!node->rchild->empty)
            {
                q[count] = node->rchild;
                count += 1;
            }
        }
    }

    int sum(int i, int j)
    {
        i -= 1, j -=1;
        int val_sum = 0, sweet_sum = 0;
        q[0] = tree;
        int count = 1;
        while (count)
        {
            Node* node = q[count - 1];
            count -= 1;
            if (node->l >= i && node->r <= j)
            {
                val_sum += node->val;
                sweet_sum += node->sweet;
                continue;
            }
            if (node->l > j || node->r < i) continue;
            if (!node->lchild->empty)
            {
                q[count] = node->lchild;
                count += 1;
            }
            if (!node->rchild->empty)
            {
                q[count] = node->rchild;
                count += 1;
            }
        }
        int ret = (sweet_sum - i * val_sum) * (i % 2 ? -1 : 1);
        return ret;
    }
};

int nums[100005];

int main()
{
    int T;
    scanf("%d", &T);

    for (int t = 1; t <= T; t += 1)
    {
        int n, q;
        scanf("%d %d", &n, &q);
        for (int i = 0; i < n; i += 1) scanf("%d", nums + i);

        Tree tree(nums, n);
        int ret = 0;
        for (int i = 0; i < q; i += 1)
        {
            char action;
            int a, b;
            scanf("%c %d %d", &action, &a, &b);
            if (action == 'Q') ret += tree.sum(a, b);
            else if (action == 'U') tree.update(a, b);
        }
        cout << "Case #" << t << ": " << ret << endl;
    }
}