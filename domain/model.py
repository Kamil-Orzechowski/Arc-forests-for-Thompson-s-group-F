from functools import reduce


class Tree:
    def __init__(self, left_child, right_child, interval=None):
        if not left_child:
            self.interval = interval
            self.is_leaf = True
        else:
            self.interval = (left_child.interval[0], right_child.interval[1])
            if left_child.is_leaf and right_child.is_leaf and right_child.interval[1] - left_child.interval[0] == 2 * (
                    left_child.interval[1] - left_child.interval[0]):
                self.is_leaf = True
            else:
                self.is_leaf = False
                self.left_child = left_child
                self.right_child = right_child

    def join(self, tree):
        return Tree(self, tree)

    def divide(self):
        if self.is_leaf:
            left_end, right_end = self.interval[0], self.interval[1]
            middle = (right_end + left_end) / 2
            tree1 = Tree(None, None, (left_end, middle))
            tree2 = Tree(None, None, (middle, right_end))
            return tree1, tree2
        else:
            return self.left_child, self.right_child

    def get_intervals(self):
        if self.is_leaf:
            return [self.interval]
        return self.left_child.get_intervals() + [self.interval] + self.right_child.get_intervals()


class Leaf(Tree):
    def __init__(self, interval):
        super().__init__(None, None, interval)


class Diagram:
    def __init__(self, forest):
        self.forest = forest
        self.basepoint = self.get_tree(0).interval[0]
        self.reduce()

    def get_tree(self, index):
        forest = self.forest
        if index in forest:
            return forest[index]
        else:
            for key in sorted(forest.keys()):
                if index < key:
                    translation = forest[key].interval[0] - key
                    return Leaf((index + translation, index + translation + 1))
        max_key = max(forest.keys())
        translation = forest[max_key].interval[1] - max_key
        return Leaf((index + translation - 1, index + translation))

    def get_intervals(self, maximal_only=False):
        min_key, max_key = min(*self.forest.keys(), 0), max(*self.forest.keys(), 0)
        if maximal_only:
            return [self.get_tree(index).interval for index in range(min_key, max_key + 1)]
        intervals = []
        for index in range(min_key, max_key + 1):
            intervals += self.get_tree(index).get_intervals()
        return intervals    

    def reduce(self):
        forest = self.forest
        for key in sorted(forest.keys()):
            tree = forest[key]
            if tree.is_leaf and tree.interval[1] - tree.interval[0] == 1:
                del forest[key]
        if not forest:
            self.forest = {0: Leaf((self.basepoint, self.basepoint + 1))}

    def apply_letter(self, letter):
        forest = self.forest
        new_forest = {}
        if letter == 'A':
            for key in forest:
                new_forest[key - 1] = forest[key]
        elif letter == 'a':
            for key in forest:
                new_forest[key + 1] = forest[key]
        elif letter == 'B':
            for key in forest:
                if key < 0:
                    new_forest[key] = forest[key]
                if key > 1:
                    new_forest[key - 1] = forest[key]
            new_forest[0] = self.get_tree(0).join(self.get_tree(1))
        elif letter == 'b':
            for key in forest:
                if key < 0:
                    new_forest[key] = forest[key]
                if key > 0:
                    new_forest[key + 1] = forest[key]
            new_forest[0], new_forest[1] = self.get_tree(0).divide()
        else:
            raise Exception('Invalid input')
        return Diagram(new_forest)

    def apply_word(self, string):
        return reduce(lambda diagram, letter: diagram.apply_letter(letter), string, self)


trivial_diagram = Diagram({0: Leaf((0, 1))})
