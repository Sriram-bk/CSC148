from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.

    === Attributes ===
    @type _marker : list[list[str]]
        Current configuration of the grid of pegs.
    @type _marker_set : set[str]
        Set indicating allowed markers.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = []
        >>> grid1.append(['*','*','*','#'])
        >>> grid1.append(['*','*','.','*'])
        >>> grid1.append(['#','*','*','*'])
        >>> g1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = []
        >>> grid2.append(['*','*','*','#'])
        >>> grid2.append(['*','*','.','*'])
        >>> grid2.append(['#','*','*','*'])
        >>> g2 = GridPegSolitairePuzzle(grid2 , {"*", ".", "#"})
        >>> g1.__eq__(g2)
        True
        >>> grid3 = []
        >>> grid3.append(['#','*','*','#'])
        >>> grid3.append(['*','.','.','*'])
        >>> grid3.append(['#','*','*','#'])
        >>> g3 = GridPegSolitairePuzzle(grid3 , {"*", ".", "#"})
        >>> g1.__eq__(g3)
        False
        """

        return (type(other) == type(self) and other._marker == self._marker and
                other._marker_set == self._marker_set)

    def __str__(self):
        """
        Return a human-readable string representation of
        GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = []
        >>> grid.append(['#', '*', '*', '*', '#'])
        >>> grid.append(['*', '*', '*', '*', '*'])
        >>> grid.append(['*', '*', '.', '*', '*'])
        >>> grid.append(['*', '*', '*', '*', '*'])
        >>> grid.append(['#', '*', '*', '*', '#'])
        >>> g = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(g)
        # * * * #
        * * * * *
        * * . * *
        * * * * *
        # * * * #
        <BLANKLINE>
        """

        rows = [" ".join(row) for row in self._marker]
        return "\n".join(rows)+"\n"

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self:
        @rtype: list[GridPegSolitaire]

        >>> grid = []
        >>> grid.append(['#', '*', '*', '*', '#'])
        >>> grid.append(['*', '*', '*', '*', '*'])
        >>> grid.append(['*', '*', '.', '*', '*'])
        >>> grid.append(['*', '*', '*', '*', '*'])
        >>> grid.append(['#', '*', '*', '*', '#'])
        >>> g = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> ext = g.extensions()
        >>> for e in ext : print(e)
        # * * * #
        * * * * *
        . . * * *
        * * * * *
        # * * * #
        <BLANKLINE>
        # * . * #
        * * . * *
        * * * * *
        * * * * *
        # * * * #
        <BLANKLINE>
        # * * * #
        * * * * *
        * * * . .
        * * * * *
        # * * * #
        <BLANKLINE>
        # * * * #
        * * * * *
        * * * * *
        * * . * *
        # * . * #
        <BLANKLINE>
        """

        # Number of Rows
        n = len(self._marker)
        # Number of Columns
        m = len(self._marker[0])

        def grid_as_list(grid):
            """
            Convert a list of depth 2, grid, to a flat list.
            Return the flat list representation of grid.

            @type grid: list[list[str]]
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
            GridPegSolitairePuzzle of grid.

            @type grid_list: list[str]
            @rtype: GridPegSolitairePuzzle
            """

            puzzle_grid = []
            # Get each row
            for i in range(0, len(grid_list), m):
                puzzle_grid_row = []
                # Get elements in each row
                for j in range(i, i + m):
                    puzzle_grid_row.append(grid_list[j])
                puzzle_grid.append(puzzle_grid_row)

            return GridPegSolitairePuzzle(puzzle_grid, self._marker_set)

        grid_list = grid_as_list(self._marker)

        # legal extensions consist of all configurations that can be reached
        # by making a single jump from this configuration.
        legal_extensions = []

        # Find every empty space in grid.
        for i in range(len(grid_list)):
            if grid_list[i] == '.':
                # Get the position of empty space in the flat list.
                index = i
                # Get the row and column index of the empty space in the grid.
                row_index = index // n
                column_index = index % m
                for j in range(-1, 2, 2):
                    list_copy = grid_list[:]
                    # Check whether two spaces to the left or the right of the
                    # empty space is within the grid.
                    if 0 <= (column_index + (2 * j)) < m:
                        # Make a move if there are two consecutive pegs to the
                        # left or to the right of the empty space.
                        if list_copy[index + (2 * j)] == '*' and \
                         list_copy[index + j] == '*':
                            list_copy[index] = '*'
                            list_copy[index + j] = '.'
                            list_copy[index + (2 * j)] = '.'
                            # Append GridPegSolitairePuzzle of list_copy
                            legal_extensions.append(list_as_grid(list_copy))

                    list_copy = grid_list[:]
                    # Check whether two spaces above or below the
                    # empty space is within the grid.
                    if 0 <= (row_index + (2 * j)) < n:
                        # Make a move if there are two consecutive pegs above
                        # below the empty space.
                        if list_copy[index + (2 * j * m)] == '*' and\
                         list_copy[index + j * m] == '*':
                            list_copy[index] = '*'
                            list_copy[index + (j * m)] = '.'
                            list_copy[index + (2 * j * m)] = '.'
                            # Append GridPegSolitairePuzzle of list_copy
                            legal_extensions.append(list_as_grid(list_copy))

        return legal_extensions

    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = []
        >>> grid1.append(['.', '.', '.', '.'])
        >>> grid1.append(['.', '.', '.', '.'])
        >>> grid1.append(['.', '*', '.', '.'])
        >>> grid1.append(['.', '.', '.', '.'])
        >>> g1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> g1.is_solved()
        True
        >>> grid2 = []
        >>> grid2.append(['*', '.', '.', '.'])
        >>> grid2.append(['.', '.', '*', '.'])
        >>> grid2.append(['.', '*', '.', '.'])
        >>> grid2.append(['.', '.', '.', '.'])
        >>> g2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> g2.is_solved()
        False
        """

        peg_count = 0

        # Iterate through each row in grid
        for row in self._marker:
            # Iterate through each element in row and count number of pegs in
            # row.
            for element in row:
                if element == '*':
                    peg_count += 1

        # A configuration is solved when there is exactly one "*" left
        return peg_count == 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
