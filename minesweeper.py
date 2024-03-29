import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        """ 
        Creating board using list and initializing other variables.
        """
        
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def is_mine(self, cell):
        """
        Tells whether a cell is mine or not.
        """
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        """
        Initializing set and variable based on given arguments.
        """
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        """
        Check whether 2 sentences are equivalent or not.
        """
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        """
        Returns a string representation of sentence.
        """
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        s = set()
        if len(self.cells) == self.count and self.count != 0:
            s = (self.cells).copy()
        return s

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        s = set()
        if self.count == 0:
            s = (self.cells).copy()
        return s

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)

class MinesweeperAI():
    """
    Minesweeper game player ( AI )
    """

    def __init__(self, height=8, width=8):
        """
        Initializing the required sets and variables.
        """
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function does the following:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.safes.add(cell)
        
        s = set()
        
        # Adding only those cells to the set about which we have no knowledge presently.
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                
                tup = (i,j)
                # Adding cell which is neither mine nor safe
                if 0 <= i < self.height and 0 <= j < self.width and tup not in self.safes:
                    if tup in self.mines:
                        count -= 1
                    else:
                        s.add(tup)
      
        # Adding only the non-empty sentence.
        if len(s) != 0:
            sentence = Sentence(s,count)
            self.knowledge.append(sentence)
        
        # Checking if any inference can be made based on existing knowledge base.
        for i in self.knowledge:
            cc = Sentence(i.cells,i.count)
            if len(cc.cells) == cc.count and cc.count != 0:
                for j in cc.cells:
                    self.mark_mine(j)
            elif cc.count == 0 and len(cc.cells) != 0:
                for j in cc.cells:
                    self.mark_safe(j)

        # Removing those sentences from knowledge base which have empty cells set.            
        cp = (self.knowledge).copy()
        for i in cp:
            if len(i.cells) == 0:
                self.knowledge.remove(i)
       
        # Adding more unique sentences based on set difference.
        cp = (self.knowledge).copy()
        for i in cp:
            for j in cp:  
                if i.__eq__(j) == False:
                    a = (i.cells).copy()
                    b = (j.cells).copy()     
                    if a.issubset(b) == True:
                        tt = set(b-a)
                        if len(tt) != 0 and (j.count-i.count) >= 0:
                            ss = Sentence(tt,j.count-i.count)
                            self.knowledge.append(ss)
        
        # Removing duplicate sentences from self.knowledge.
        res = [] 
        for i in self.knowledge: 
            if i not in res: 
                res.append(i) 
        self.knowledge = res
  
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        move = None
        for i in self.safes:
            if i not in self.moves_made:
                move = i
                break
        return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        s = set()
        for i in range(self.height):
            for j in range(self.width):
                tup = (i,j)
                s.add(tup)
        for i in self.moves_made:
            if i in s:
                s.discard(i)
        for i in self.mines:
            if i in s:
                s.discard(i)
        move = None
        if len(s) != 0:
            move = random.choice(tuple(s))
        return move

