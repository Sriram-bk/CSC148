from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.

    === Attributes ===
    @type from_grid : tuple[tuple(str)]]
        Current configuration of grid
    @type to_grid : tuple[tuple(str)]]
        Final solution configuration of grid
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle
        @rtype: bool

        >>> grid1 = (('1', '2', '3'), ('4', '*', '5' ))
        >>> grid2 = (('1', '2', '3'), ('4', '*', '5' ))
        >>> grid3 = (('2', '1', '4'), ('5', '*', '3' ))
        >>> mnp1 = MNPuzzle(grid1, grid3)
        >>> mnp2 = MNPuzzle(grid2, grid3)
        >>> mnp1.__eq__(mnp2)
        True
        >>> mnp3 = MNPuzzle(grid3, grid1)
        >>> mnp1.__eq__(mnp3)
        False
        """

        return (type(other) == type(self) and other.from_grid ==
                self.from_grid and other.to_grid == self.to_grid)

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> grid1 = (('1', '2', '3'), ('4', '*', '5' ))
        >>> grid2 = (('2', '1', '4'), ('5', '*', '3' ))
        >>> mnp = MNPuzzle(grid1, grid2)
        >>> print(mnp)
        From Grid :
        1 2 3
        4 * 5
        <BLANKLINE>
        To Grid :
        2 1 4
        5 * 3
        """

        def grid_rep(grid):
            """
            Return a human-readable string representation of grid.

            @type grid: tuple(tuple(str))
            @rtype: str
            """
            rows = [" ".join(row) for row in grid]
            return "\n".join(rows)

        return "From Grid :\n" + grid_rep(self.from_grid) + "\n\n" + \
               "To Grid :\n" + grid_rep(self.to_grid)

    def extensions(self):
        """

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> grid1 = (('1', '2', '3'), ('4', '*', '5' ), ('6', '7', '8'))
        >>> grid2 = (('2', '1', '4'), ('5', '*', '3' ), ('6', '7', '8'))
        >>> mnp = MNPuzzle(grid1, grid2)
        >>> ext = mnp.extensions()
        >>> for e in ext : print(e)
        From Grid :
        1 2 3
        * 4 5
        6 7 8
        <BLANKLINE>
        To Grid :
        2 1 4
        5 * 3
        6 7 8
        From Grid :
        1 * 3
        4 2 5
        6 7 8
        <BLANKLINE>
        To Grid :
        2 1 4
        5 * 3
        6 7 8
        From Grid :
        1 2 3
        4 5 *
        6 7 8
        <BLANKLINE>
        To Grid :
        2 1 4
        5 * 3
        6 7 8
        From Grid :
        1 2 3
        4 7 5
        6 * 8
        <BLANKLINE>
        To Grid :
        2 1 4
        5 * 3
        6 7 8
        """

        def grid_as_list(grid):
            """
            Convert a tuple of depth 2, grid, to a flat list.
            Return the flat list representation of grid.

            @type grid: tuple[tuple[str]]
            @rtype: list[str]
            """

            grid_list = []

            for row in grid:
                for item in row:
                    grid_list.append(item)

            return grid_list

        def list_as_grid(grid_list):
            """
            Convert a flat list, grid_list, to a grid and return
            MNPuzzle of grid.

            @type grid_list: list[str]
            @rtype: MNPuzzle
            """

            puzzle_grid = ()
            for i in range(0, len(grid_list), self.m):
                puzzle_grid_row = ()
                for j in range(i, i + self.m):
                    puzzle_grid_row += (grid_list[j],)
                puzzle_grid += (puzzle_grid_row,)

            return MNPuzzle(puzzle_grid, self.to_grid)

        grid_list = grid_as_list(self.from_grid)

        # legal extensions are configurations that can be reached by swapping
        # one symbol to the left, right, above, or below "*" with "*"
        legal_extensions = []

        # Get the position of empty space in the flat list.
        index = grid_list.index('*')
        # Get the row and column index of the empty space in the grid.
        row_index = index // self.n
        column_index = index % self.m

        for i in range(-1, 2, 2):
            list_copy = grid_list[:]
            # Check whether the space to the left or the right of the
            # empty space is within the grid and make move.
            if 0 <= (column_index + i) < self.m:
                list_copy[index], list_copy[index + i] = \
                 list_copy[index + i], list_copy[index]
                # Append MNPuzzle of list_copy
                legal_extensions.append(list_as_grid(list_copy))

            list_copy = grid_list[:]
            # Check whether the space above or below the
            # empty space is within the grid and make move.
            if 0 <= (row_index + i) < self.n:
                list_copy[index], list_copy[index + (i * self.m)] = \
                 list_copy[index + (i * self.m)], list_copy[index]
                # Append MNPuzzle of list_copy
                legal_extensions.append(list_as_grid(list_copy))

        return legal_extensions

    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @type self : MNPuzzle
        @rtype: bool

        >>> grid1 = (('1', '2', '3'), ('4', '*', '5' ), ('6', '7', '8'))
        >>> grid2 = (('2', '1', '4'), ('5', '*', '3' ), ('6', '7', '8'))
        >>> grid3 = (('1', '2', '3'), ('4', '*', '5' ), ('6', '7', '8'))
        >>> mnp1 = MNPuzzle(grid1, grid2)
        >>> mnp1.is_solved()
        False
        >>> mnp2 = MNPuzzle(grid1, grid3)
        >>> mnp2.is_solved()
        True
        """

        # MNPuzzle is solved when from_grid is the same as to_grid
        return self.from_grid == self.to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
