class PieceRep:
    # Diese Klasse stellt die logische Repräsentation einer Spielfigur auf dem Tic-Tac-Toe Feld dar
    # Die Nummer des Spielers kennzeichnet dabei, welcher Spieler die Figur gesetzt hat
    # Der Rang symbolisiert welche Größe die Spielfigur hat (klein, mittel, groß)

    def __init__(self, player_number, rank):
        self.player_number = player_number
        self.rank = rank

    def __str__(self):
        return 'Player[' + str(self.player_number) + '], Rang der Figur: ' + str(self.rank) + ' '

    def get_player_number(self):
        return self.player_number
