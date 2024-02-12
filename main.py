class Board:

    def __init__(self, cells, rules_row, rules_column):
        Board.assert_rules(rules_row, rules_column, cells)
        self.set_cells(cells)
        self.set_rules(rules_row, rules_column)
        self.set_perspective("row")

    def get_cells(self):
        return self.cells
 
    def get_rules(self, perspective):
        Board.assert_perspective(perspective)
        return self.rules[perspective]
    
    def get_perspective(self):
        return self.perspective
    
    def get_line(self, index, perspective):
        Board.assert_perspective(perspective)
        cells = self.get_cells() if perspective == self.get_perspective() else self.transpose_cells()
        return cells[index]
    
    def get_num_lines(self):
        return len(self.get_cells())

    def get_size(self):
        return (self.get_num_lines(), ) * 2
    
    def get_num_cells(self):
        return self.get_num_lines() ** 2
    
    def set_cells(self, cells):
        Board.assert_cells(cells)
        self.cells = cells
    
    def set_rules(self, rules_row, rules_column):
        Board.assert_rules(rules_row, rules_column, self.get_cells())
        self.rules = {"row": rules_row, "column": rules_column}
    
    def set_perspective(self, perspective):
        Board.assert_perspective(perspective)
        self.perspective = perspective
    
    def set_line(self, line, index, perspective):
        Board.assert_perspective(perspective)
        same_perspective = perspective == self.get_perspective()
        cells = self.get_cells() if same_perspective else self.transpose_cells()
        self.set_cells(cells[:index] + [line] + cells[index+1:])
        if not same_perspective:
            self.set_cells(self.transpose_cells())
        
    def toggle_perspective(self):
        self.set_perspective("column" if self.get_perspective == "row" else "row")
    
    def transpose_cells(self):
        self.toggle_perspective()
        return ["".join([row[i] for row in self.get_cells()]) for i in range(len(self.get_cells()[0]))]
    
    def display_cells(self):
        print("\n".join(self.get_cells()))

    @staticmethod
    def assert_cells(cells):
        assert all(len(row) == len(cells[0]) for row in cells), "The number of columns in each row must be the same."
        num_rows = len(cells)
        num_columns = len(cells[0])
        assert num_rows == num_columns, "The number of both rows and columns must be the same."
    
    @staticmethod
    def assert_rules(rules_row, rules_column, cells):
        Board.assert_cells(cells)
        num_rules_row = len(rules_row)
        num_rules_column = len(rules_column)
        assert num_rules_row == num_rules_column, "The number of vertical rules must be equal to the number of horizontal rules."
        assert len(cells) == num_rules_row, "The number of rules must be equal to the the number of rows or columns."
    
    @staticmethod
    def assert_perspective(perspective):
        assert perspective in ["row", "column"], "The perspective value must be either row or column."

class Game:

    def __init__(self, board):
        self.board = board
    
    def get_board(self):
        return self.board
    
    @staticmethod
    def generate_line(line, rule):
        lines = []

        # find all possible lines
        def fill_blank(line_draft):
            if "_" not in line_draft:
                # check if the generated line is correct by the rule
                if tuple([n for n in list(map(len, line_draft.split("0"))) if n != 0]) == rule:
                    lines.append(line_draft)
            else:
                blank_index = line_draft.index("_")

                line_draft = f"{line_draft[:blank_index]}1{line_draft[blank_index+1:]}"
                fill_blank(line_draft)

                line_draft = f"{line_draft[:blank_index]}0{line_draft[blank_index+1:]}"
                fill_blank(line_draft)
        
        fill_blank(line)

        # find the common traits in each possible line
        final_line = "".join([lines[0][ci] if all(lines[li][ci] == lines[0][ci] for li in range(len(lines))) else "_" for ci in range(len(lines[0]))])
        return final_line
    
    def solve(self):
        while any("_" in row for row in self.get_board().get_cells()):
            for perspective in ["row", "column"]:
                for index in range(self.get_board().get_num_lines()):
                    board = self.get_board()
                    self.get_board().set_line(Game.generate_line(board.get_line(index, perspective), board.get_rules(perspective)[index]), index, perspective)
                    
ce = ["_" * 15] * 15
r = [(2, ), (1, 2), (4, 2, 4), (1, 2, 4, 2), (1, 1, 2, 2), (5, 2, 2), (1, 2, 7), (1, 11), (13, 1), (7, 3, 1), (7, 2, 1), (12, ), (9, ), (9, ), (5, )]
co = [(2, ), (2, 3), (2, 1, 5), (1, 2, 4, 1), (1, 9), (13, ), (1, 8), (1, 2, 5), (3, 3, 4), (1, 7, 4), (2, 11), (3, 8), (1, 5, 2), (6, 2), (2, 4)]

g = Game(Board(ce, r, co))
g.solve()
g.get_board().display_cells()