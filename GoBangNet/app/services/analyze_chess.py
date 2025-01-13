

class analyze_chess(object):

    def __init__(self,pieces):
        self.pieces = pieces

    # def move(self):
    #     from app.main import AIPlayer
    #     index = AIPlayer.get_move(self.pieces)
    #     return index
    #
    # def low_move(self):
    #     from app.main import AIPlayer_low
    #     index = AIPlayer_low.get_move(self.pieces)
    #     return index
    #
    # def bad_move(self):
    #     from app.main import AIPlayer_Bad
    #     index = AIPlayer_Bad.get_move(self.pieces)
    #     return index

    def move_1000(self):
        from app.main import  AIPlayer_1000
        index = AIPlayer_1000.get_move(self.pieces)
        return index

    def move_2000(self):
        from app.main import AIPlayer_2000
        index = AIPlayer_2000.get_move(self.pieces)
        return index

    def move_3000(self):
        from app.main import AIPlayer_3000
        index = AIPlayer_3000.get_move(self.pieces)
        return index

    def move_5000(self):
        from app.main import AIPlayer_5000
        index = AIPlayer_5000.get_move(self.pieces)
        return index

