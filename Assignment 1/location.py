class Location:
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        self.row = int(row)
        self.column = int(column)

    def __str__(self):
        """Return a string representation.

        @rtype: str
        """
        return "({},{})".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool
        """

        if (self.row == other.row) and (self.column == other.column):
            return True
        else:
            return False


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    """
    return (abs(origin.row - destination.row) + abs(origin.column -
                                                    destination.column))


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    """
    comma_index = location_str.index(',')
    return Location(location_str[0:comma_index], location_str[comma_index + 1:])
