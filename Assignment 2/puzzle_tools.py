"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    # TA Asher helped with idea behind DFS
    root_node = PuzzleNode(puzzle)
    visited = set()
    stack = deque()
    stack.append(root_node)

    while len(stack) != 0:
        node = stack.pop()
        if str(node.puzzle) not in visited:
            visited.add(str(node.puzzle))
            if node.puzzle.is_solved():
                # If puzzle has been solved return a path to the solution
                # from the original puzzle.
                path = get_path(node)
                return path
            elif not node.puzzle.fail_fast():
                exts = [PuzzleNode(extension, [], node) for extension in
                        node.puzzle.extensions() if str(extension) not in
                        visited]
                # Extend all extensions of node.puzzle that haven't been
                # visited.
                stack.extend(exts)

    return None


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    root_node = PuzzleNode(puzzle)
    deck = deque()
    deck.append(root_node)
    visited = set()

    # TA Asher helped with idea behind BFS
    while len(deck) != 0:
        node = deck.popleft()
        if str(node.puzzle) not in visited:
            visited.add(str(node.puzzle))
            if node.puzzle.is_solved():
                # If puzzle has been solved return a path to the solution
                # from the original puzzle.
                path = get_path(node)
                return path
            else:
                # Extend all extensions of node.puzzle that haven't been
                # visited.
                deck.extend([PuzzleNode(extension, [], node) for extension in
                             node.puzzle.extensions() if str(extension) not in
                             visited])

    return None


def get_path(node):
    """
    Return a path from a puzzle to the solution, node.

    @type node: PuzzleNode
    @rtype: PuzzleNode

    """
    curr_node = node
    parent = curr_node.parent
    while parent is not None:
        # Append curr_node to parent
        parent.children.append(curr_node)
        # Set curr_node to parent and then set parent to the parent of the
        # curr_node.
        curr_node = parent
        parent = curr_node.parent
    return curr_node


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
