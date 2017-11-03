from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.

    === Attributes ===
    @type _from_word : str
        Current word.
    @type _to_word : str
        Final word to get to.
    @type _word_set : set[str]
        Set of words that can be used to get to the final word.
    @type _chars :
        Set of charecters that can be used to change _from_word.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self : WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool

        >>> words = open("words", "r")
        >>> word_set = set(words.read().split())
        >>> w1 = WordLadderPuzzle('comic', 'tonic', word_set)
        >>> w2 = WordLadderPuzzle('comic', 'tonic', word_set)
        >>> w1.__eq__(w2)
        True
        >>> w3 = WordLadderPuzzle('atomic', 'iconic', word_set)
        >>> w1.__eq__(w3)
        False
        """

        return (type(other) == type(self) and other._from_word ==
                self._from_word and other._to_word == self._to_word and
                other._word_set == self._word_set)

    def __str__(self):
        """
        Return a human-readable string representation of WordLadderPuzzle
        self.

        @type self : WordLadderPuzzle
        @rtype: str

        >>> words = open("words", "r")
        >>> word_set = set(words.read().split())
        >>> w = WordLadderPuzzle('cast','make', word_set)
        >>> print(w)
        From word : cast
        To word : make
        """

        return "From word : {}\nTo word : {}".format(self._from_word,
                                                     self._to_word)

    def extensions(self):
        """ Return list of extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> words = open("words", "r")
        >>> word_set = set(words.read().split())
        >>> w = WordLadderPuzzle('no','on', word_set)
        >>> legal_extensions = w.extensions()
        >>> for extension in legal_extensions: print(extension)
        From word : do
        To word : on
        From word : go
        To word : on
        From word : ho
        To word : on
        From word : lo
        To word : on
        From word : so
        To word : on
        From word : to
        To word : on
        From word : yo
        To word : on
        From word : nu
        To word : on
        """

        # convenient names
        from_word, word_set, chars = self._from_word, self._word_set,\
            self._chars

        # legal extensions are WordLadderPuzzles that have a
        # from_word that can be reached from this one by changing a single
        # letter to one of those in self._chars
        legal_extensions = []

        # Iterate through the word and change every letter in _from_word
        # to all the letters in chars one at a time.
        for index in range(len(from_word)):
            for char in chars:
                word = from_word[0:index] + char + from_word[index + 1:]

                # If word is in the word_set then append WordLadderPuzzle
                # to the legal extensions.
                if word in word_set and char != from_word[index]:
                    wlp = WordLadderPuzzle(word, self._to_word, word_set)
                    legal_extensions.append(wlp)

        return legal_extensions

    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> words = open("words", "r")
        >>> word_set = set(words.read().split())
        >>> w1 = WordLadderPuzzle('cast','cast', word_set)
        >>> w2 = WordLadderPuzzle('cast','make', word_set)
        >>> w1.is_solved()
        True
        >>> w2.is_solved()
        False
        """

        # WordLadderPuzzle is solved when _from_word is the
        # same as _to_word.
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
