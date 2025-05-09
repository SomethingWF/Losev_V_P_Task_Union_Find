class DisjointSetUnionRank:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0

    def find(self, item):
        if item not in self.parent:
            self.make_set(item)  # Автоматически создаем множество, если элемент новый
            return item

        if self.parent[item] == item:
            return item
        else:
            self.parent[item] = self.find(self.parent[item])
            return self.parent[item]

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        
        return False
    
# if __name__ == "__main__":
#     dsu = DisjointSetUnionRank()

#     elements = [0, 1, 2, 3, 4, 5, 6]
#     for elem in elements:
#         dsu.make_set(elem)
#     dsu.union(1, 2)
#     dsu.union(1, 3)
#     dsu.union(5, 4)
#     dsu.union(6, 4)
#     dsu.union(6, 3)
#     print(dsu.find(3), dsu.parent)