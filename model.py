from functools import reduce, lru_cache
from itertools import product


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


class Leaf(Tree):
    def __init__(self, interval):
        super().__init__(None, None, interval)


class Diagram:
    def __init__(self, forest: dict[int, Tree]):
        self.forest = forest

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
        elif letter.lower() == 'c':
            return self
        else:
            raise Exception('Invalid input')
        return Diagram(new_forest)

    def apply_word(self, string):
        return reduce(lambda diagram, letter: diagram.apply_letter(letter), string, self)


def describe_action(diagram, string):
    created_arcs, deleted_arcs = [], []
    rightmost_moved = None
    created, deleted = False, False
    first_creation_index, first_deletion_index = -1, -1

    for index in range(len(string)):
        letter = string[index]
        if letter == 'B':
            new_arc = (diagram.get_tree(0).interval[0], diagram.get_tree(1).interval[1])
            created_arcs.append(new_arc)
            if not rightmost_moved or tuple(reversed(new_arc)) > tuple(reversed(rightmost_moved)):
                rightmost_moved = new_arc
                first_creation_index, first_deletion_index = index, -1
                created, deleted = True, False
            elif new_arc == rightmost_moved:
                if not created:
                    first_creation_index = index
                    created = True
        if letter == 'b':
            deleted_arc = diagram.get_tree(0).interval
            deleted_arcs.append(deleted_arc)
            if not rightmost_moved or tuple(reversed(deleted_arc)) > tuple(reversed(rightmost_moved)):
                rightmost_moved = deleted_arc
                first_creation_index, first_deletion_index = -1, index
                created, deleted = False, True
            elif deleted_arc == rightmost_moved:
                if not deleted:
                    first_deletion_index = index
                    deleted = True
        diagram = diagram.apply_letter(letter)

    B_special_index = first_creation_index if (0 <= first_creation_index < first_deletion_index
                                               or first_deletion_index == -1) else None
    b_special_index = first_deletion_index if 0 <= first_deletion_index else None

    return {'created arcs': created_arcs, 'deleted_arcs': deleted_arcs, 'rightmost_moved': rightmost_moved,
            'B_special_index': B_special_index, 'b_special_index': b_special_index}


trivial_diagram = Diagram({0: Leaf((0, 1))})


def describe(string):
    return describe_action(trivial_diagram, string)


def print_description(string):
    print(describe(string))


@lru_cache(maxsize=None)
def get_special_letters(string):
    return describe(string)['B_special_index'], describe(string)['b_special_index']


def get_possible_prefixes(string):
    alphabet = {'A', 'a', 'B', 'b'}
    first_letter = string[0]
    if first_letter == 'B':
        alphabet.remove('b')
    if first_letter == 'b':
        alphabet.remove('B')
    for letter in string:
        if letter == 'A' or letter == 'a':
            alphabet.remove(letter)
            break
    return alphabet


def get_possible_suffixes(string):
    return get_possible_prefixes(''.join(reversed(string)))


class Word:
    def __init__(self, string: str):
        self.string = string
        self.expanded = string.replace('c', 'Aa')
        self.B_special, self.b_special = get_special_letters(string)
        self.specials = set(filter(lambda x: x is not None, (self.B_special, self.b_special)))
        self.with_dots = ''.join(string[i] + '.' if i in self.specials else string[i] for i in range(len(string)))
        self.without_specials = ''.join(string[i] for i in set(range(len(string))).difference(self.specials))

    def __eq__(self, other):
        return self.string == other.string

    def __hash__(self):
        return hash(self.string)

    def test_extension(self, prefix, suffix):
        new_str = prefix + self.string + suffix
        return all(i + 1 in get_special_letters(new_str) for i in self.specials)

    def insert_c(self):
        return Word(self.string.replace('c', 'cc', 1))

    def get_derived_words(self, c_insertion: bool):
        word_list = []
        for prefix, suffix in product(get_possible_prefixes(self.expanded), get_possible_suffixes(self.expanded)):
            if self.test_extension(prefix, suffix):
                word_list.append(Word(prefix + self.string + suffix))
        if 'c' in self.string and c_insertion:
            with_c_inserted = [word.insert_c() for word in word_list]
            word_list += with_c_inserted
        return word_list
