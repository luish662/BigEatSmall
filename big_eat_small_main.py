import sys
import pygame as pg
import pygame.display
from button import Button
from piece_rep import PieceRep

pg.init()

# Laden der Music und Sounds
pygame.mixer.music.load("resources/8_Bit_Retro_Funk.mp3")
button_bling = pygame.mixer.Sound("resources/button_bling.wav")
pick_up_piece = pygame.mixer.Sound("resources/pick_up_piece.wav")
pygame.mixer.music.play(loops=-1)
music_playlist = ["resources/8_Bit_Retro_Funk.mp3", 'resources/Land_of_8_Bits.mp3', "resources/pigstep.mp3",
                  "resources/Snake Man Stage.mp3"]
current_playing_song = 0

background_list = ["resources/Background.png", "resources/red_space.jpg", "resources/blue_space.jpg",
                   "resources/city.jpg"]
current_bg = 0
BG = pg.image.load('resources/Background.png')

SCREEN = pg.display.set_mode((1280, 720))
pg.display.set_caption('Main-Menu')
players_turn = '1'
selected_piece = None


def get_font(size):
    return pygame.font.Font("resources/font.ttf", size)


def change_music():
    # Ändert die Musik durch Spielen des jeweils nächsten Songs in der Playlist
    global current_playing_song
    if current_playing_song < len(music_playlist) - 1:
        current_playing_song += 1
    else:
        current_playing_song = 0
    pygame.mixer.music.load(music_playlist[current_playing_song])
    pygame.mixer.music.play(loops=-1)


def change_background():
    # Ändert den Hintergrund zum nächsten in der Hintergrundliste
    global BG
    global current_bg
    if current_bg < len(background_list) - 1:
        current_bg += 1
    else:
        current_bg = 0
    BG = pg.image.load(background_list[current_bg])


def versus_mode():
    # Spiele den Versus Mode mit zwei Spielern
    display_width = 700
    display_height = 700

    black = (0, 0, 0)
    white = (255, 255, 255)

    # Logische Repräsentation des Tic-Tac-Toe Spielfeldes
    board = [[None] * 3, [None] * 3, [None] * 3]

    SCREEN = pg.display.set_mode((display_width, display_height))
    pg.display.set_caption('Versus Mode')
    clock = pg.time.Clock()

    crashed = False

    # Laden der Bild und Musikressourcen
    p1_big_image = pg.image.load('resources/Player1Big.png')
    p1_medium_image = pg.image.load('resources/Player1Medium.png')
    p1_small_image = pg.image.load('resources/Player1Small.png')
    p2_big_image = pg.image.load('resources/Player2Big.png')
    p2_medium_image = pg.image.load('resources/Player2Medium.png')
    p2_small_image = pg.image.load('resources/Player2Small.png')

    p1_big_pos = ((display_width * 0.3), (display_height - 70))
    p1_medium_pos = ((display_width * 0.5), (display_height - 70))
    p1_small_pos = ((display_width * 0.7), (display_height - 70))
    p2_big_pos = ((display_width * 0.7), (display_height - (display_height - 70)))
    p2_medium_pos = ((display_width * 0.5), (display_height - (display_height - 70)))
    p2_small_pos = ((display_width * 0.3), (display_height - (display_height - 70)))

    SCREEN.blit(BG, (0, 0))

    # zeichnen des Tic-Tac-Toe-Feldes
    # zeichnen der vertikalen Linien
    pg.draw.line(SCREEN, white, (display_width / 5 * 2, display_height / 5),
                 (display_width / 5 * 2, display_height - display_height / 5), 7)

    pg.draw.line(SCREEN, white, (display_width / 5 * 3, display_height / 5),
                 (display_width / 5 * 3, display_height - display_height / 5), 7)

    # zeichnen der horizontalen Linien
    pg.draw.line(SCREEN, white, (display_width / 5, display_height / 5 * 2),
                 (display_width - display_width / 5, display_height / 5 * 2), 7)

    pg.draw.line(SCREEN, white, (display_width / 5, display_height / 5 * 3),
                 (display_width - display_width / 5, display_height / 5 * 3), 7)

    def draw_pieces(row, col):
        global players_turn
        global selected_piece

        if row == 1:
            pos_x = 210 - 50

        if row == 2:
            pos_x = 350 - 50

        if row == 3:
            pos_x = 490 - 50

        if col == 1:
            pos_y = 210 - 50

        if col == 2:
            pos_y = 350 - 50

        if col == 3:
            pos_y = 490 - 50

        piece_rep = PieceRep(players_turn, selected_piece.rank)
        board[row - 1][col - 1] = piece_rep

        if players_turn == '1':
            SCREEN.blit(selected_piece.get_image(), (pos_y, pos_x))
            pick_up_piece.play()
            players_turn = '2'
            current_count = selected_piece.text_input
            decreased_count = str(int(current_count) - 1)
            selected_piece.set_text_input(decreased_count)
            selected_piece.set_text(decreased_count)
            selected_piece.update(SCREEN)
            selected_piece = None
        else:
            SCREEN.blit(selected_piece.get_image(), (pos_y, pos_x))
            pick_up_piece.play()
            players_turn = '1'
            current_count = selected_piece.text_input
            decreased_count = str(int(current_count) - 1)
            selected_piece.set_text_input(decreased_count)
            selected_piece.set_text(decreased_count)
            selected_piece.update(SCREEN)
            selected_piece = None

        pg.display.update()

    def user_click():
        x, y = pg.mouse.get_pos()

        # Ermittelt die Spalte des Mausklicks (1-3)
        if display_width / 5 < x < display_width / 5 * 2:
            col = 1

        elif display_width / 5 * 2 < x < display_width / 5 * 3:
            col = 2

        elif display_width / 5 * 3 < x < display_width / 5 * 4:
            col = 3

        else:
            col = None

        # Ermittelt die Reihe des Mausklicks (1-3)
        if display_height / 5 < y < display_height / 5 * 2:
            row = 1

        elif display_height / 5 * 2 < y < display_height / 5 * 3:
            row = 2

        elif display_height / 5 * 3 < y < display_height / 5 * 4:
            row = 3

        else:
            row = None

        if selected_piece is not None:
            if row and col and board[row - 1][col - 1] is None or row and col and board[row - 1][
                col - 1].rank < selected_piece.rank:
                draw_pieces(row, col)
                check_win()
                check_draw()

    def check_win():
        # Überprüft, ob ein Spieler gewonnen hat
        global players_turn
        global selected_piece
        # Überprüft nach einer vollen Reihe
        for row in range(0, 3):
            if board[row][0] is not None and board[row][1] is not None and board[row][2] is not None:
                if board[row][0].player_number == board[row][1].player_number == board[row][2].player_number:
                    winner_name = 'Player ' + str(board[row][0].player_number)
                    players_turn = '1'
                    selected_piece = None
                    win_screen(winner_name)

        # Überprüft nach einer vollen Spalte
        for col in range(0, 3):
            if board[0][col] is not None and board[1][col] is not None and board[2][col] is not None:
                if board[0][col].player_number == board[1][col].player_number == board[2][col].player_number:
                    winner_name = 'Player ' + str(board[0][col].player_number)
                    players_turn = '1'
                    selected_piece = None
                    win_screen(winner_name)

        # Die folgenden zwei Bedingungen prüfen nach einer vollen Diagonalen
        if board[0][0] is not None and board[1][1] is not None and board[2][2] is not None:
            if board[0][0].player_number == board[1][1].player_number == board[2][2].player_number:
                # volle Diagonale von links nach rechts
                winner_name = 'Player ' + str(board[0][0].player_number)
                players_turn = '1'
                selected_piece = None
                win_screen(winner_name)

        if board[0][2] is not None and board[1][1] is not None and board[2][0] is not None:
            if board[0][2].player_number == board[1][1].player_number == board[2][0].player_number:
                # volle Diagonale von rechts nach links
                winner_name = 'Player ' + str(board[0][2].player_number)
                players_turn = '1'
                selected_piece = None
                win_screen(winner_name)

    def check_draw():
        # Überprüft, ob das Spiel ein unentschieden ist.
        # der Einfachheit halber wird hier geprüft, ob die Summe der Ränge aller PieceRep Objekte 24 beträgt
        # 24 ist die Summe, die entsteht, wenn alle großen Spielfiguren gesetzt wurden und auf dem Rest
        # des Spielfeldes nur mittlere stehen (3 + 3 + 3 + 3 + 3 + 3 + 2 + 2 + 2 = 24)
        # An diesem Punkt ist es für beide Spieler nicht mehr möglich einen weiteren Zug zu machen -> Unentschieden
        for field_array in board:
            for piece_rep in field_array:
                if piece_rep is None:
                    return

        if (board[0][0].rank + board[0][1].rank + board[0][2].rank + board[1][0].rank
            + board[1][1].rank + board[1][2].rank + board[2][0].rank + board[2][1].rank + board[2][2].rank) == 24:
            draw_screen()

    def versus_loop():
        # Game loop in Versus-Mode
        global SCREEN
        global selected_piece
        global players_turn

        p1_big = Button(image=p1_big_image, pos=p1_big_pos,
                        text_input="3", font=get_font(25), base_color="White", hovering_color="Green", rank=3)

        p1_medium = Button(image=p1_medium_image, pos=p1_medium_pos,
                           text_input="3", font=get_font(25), base_color="White", hovering_color="Green", rank=2)

        p1_small = Button(image=p1_small_image, pos=p1_small_pos,
                          text_input="3", font=get_font(25), base_color="White", hovering_color="Green", rank=1)

        p2_big = Button(image=p2_big_image, pos=p2_big_pos,
                        text_input="3", font=get_font(25), base_color="White", hovering_color="Green", rank=3)
        p2_medium = Button(image=p2_medium_image, pos=p2_medium_pos,
                           text_input="3", font=get_font(25), base_color="White", hovering_color="Green", rank=2)

        p2_small = Button(image=p2_small_image, pos=p2_small_pos,
                          text_input="3", font=get_font(25), base_color="White", hovering_color="Green", rank=1)

        while not crashed:
            versus_mouse_pos = pg.mouse.get_pos()

            versus_back = Button(image=None, pos=(75, 50),
                                 text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green",
                                 rank=0)

            versus_back.change_color(versus_mouse_pos)
            versus_back.update(SCREEN)

            # Damit die Spielfiguren einen Hover-Effekt haben, muss der richtige Spieler am Zug sein
            # und es muss mindestens eine jeweilige Figur da sein
            if players_turn == '1' and p1_big.text_input != '0':
                p1_big.change_color(versus_mouse_pos)
            p1_big.update(SCREEN)

            if players_turn == '1' and p1_medium.text_input != '0':
                p1_medium.change_color(versus_mouse_pos)
            p1_medium.update(SCREEN)

            if players_turn == '1' and p1_small.text_input != '0':
                p1_small.change_color(versus_mouse_pos)
            p1_small.update(SCREEN)

            if players_turn == '2' and p2_big.text_input != '0':
                p2_big.change_color(versus_mouse_pos)
            p2_big.update(SCREEN)

            if players_turn == '2' and p2_medium.text_input != '0':
                p2_medium.change_color(versus_mouse_pos)
            p2_medium.update(SCREEN)

            if players_turn == '2' and p2_small.text_input != '0':
                p2_small.change_color(versus_mouse_pos)
            p2_small.update(SCREEN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if versus_back.check_for_input(versus_mouse_pos):
                        button_bling.play()
                        players_turn = '1'
                        selected_piece = None
                        SCREEN = pg.display.set_mode((1280, 720))
                        main_menu()

                    # Es muss Spieler 1 am Zug sein
                    # Die Anzahl der Figur darf nicht 0 sein -> keine entsprechende Figur mehr übrig
                    # damit die unteren Spielfiguren ausgewählt werden können
                    elif p1_big.check_for_input(versus_mouse_pos) and players_turn == '1' \
                            and p1_big.text_input != '0':
                        pick_up_piece.play()
                        selected_piece = p1_big
                    elif p1_medium.check_for_input(versus_mouse_pos) and players_turn == '1' \
                            and p1_medium.text_input != '0':
                        pick_up_piece.play()
                        selected_piece = p1_medium
                    elif p1_small.check_for_input(versus_mouse_pos) and players_turn == '1' \
                            and p1_small.text_input != '0':
                        pick_up_piece.play()
                        selected_piece = p1_small

                    # Es muss Spieler 2 am Zug sein
                    # Die Anzahl der Figur darf nicht 0 sein -> keine entsprechende Figur mehr übrig
                    # damit die unteren Spielfiguren ausgewählt werden können
                    elif p2_big.check_for_input(versus_mouse_pos) and players_turn == '2' \
                            and p2_big.text_input != '0':
                        pick_up_piece.play()
                        selected_piece = p2_big
                    elif p2_medium.check_for_input(versus_mouse_pos) and players_turn == '2' \
                            and p2_medium.text_input != '0':
                        pick_up_piece.play()
                        selected_piece = p2_medium
                    elif p2_small.check_for_input(versus_mouse_pos) and players_turn == '2' \
                            and p2_small.text_input != '0':
                        pick_up_piece.play()
                        selected_piece = p2_small
                    else:
                        user_click()

            pg.display.update()
            clock.tick(60)

    versus_loop()


# Settings um Music, skins etc. zu ändern
def settings():
    while True:
        settings_mouse_pos = pg.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        settings_text = get_font(75).render("SETTINGS", True, '#b68f40')
        settings_rect = settings_text.get_rect(center=(640, 100))
        SCREEN.blit(settings_text, settings_rect)

        change_music_btn = Button(image=None, pos=(640, 260),
                                  text_input="CHANGE MUSIC", font=get_font(45), base_color="white",
                                  hovering_color="Green",
                                  rank=0)

        change_music_btn.change_color(settings_mouse_pos)
        change_music_btn.update(SCREEN)

        change_background_btn = Button(image=None, pos=(640, 420),
                                       text_input="CHANGE BACKGROUND", font=get_font(45), base_color="white",
                                       hovering_color="Green",
                                       rank=0)

        change_background_btn.change_color(settings_mouse_pos)
        change_background_btn.update(SCREEN)

        settings_back = Button(image=None, pos=(640, 560),
                               text_input="BACK", font=get_font(45), base_color="white", hovering_color="Green", rank=0)

        settings_back.change_color(settings_mouse_pos)
        settings_back.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if settings_back.check_for_input(settings_mouse_pos):
                    button_bling.play()
                    main_menu()
                elif change_music_btn.check_for_input(settings_mouse_pos):
                    button_bling.play()
                    change_music()
                elif change_background_btn.check_for_input(settings_mouse_pos):
                    button_bling.play()
                    change_background()

        pg.display.update()


def main_menu():
    # Main-Menu loop
    pygame.display.set_caption('Big Eat Small')

    while True:
        SCREEN.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(80).render('BIG EAT SMALL', True, '#b68f40')
        menu_rect = menu_text.get_rect(center=(640, 100))

        versus_button = Button(image=pg.image.load('resources/Play Rect.png'), pos=(640, 250),
                               text_input='VERSUS', font=get_font(60), base_color='#d7fcd4', hovering_color='white',
                               rank=0)

        settings_button = Button(image=pg.image.load('resources/Options Rect.png'), pos=(640, 400),
                                 text_input='SETTINGS', font=get_font(60), base_color='#d7fcd4', hovering_color='white',
                                 rank=0)

        quit_button = Button(image=pg.image.load('resources/Quit Rect.png'), pos=(640, 550),
                             text_input='QUIT', font=get_font(60), base_color='#d7fcd4', hovering_color='white', rank=0)

        SCREEN.blit(menu_text, menu_rect)

        for button in [versus_button, settings_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if versus_button.check_for_input(menu_mouse_pos):
                    button_bling.play()
                    versus_mode()
                if settings_button.check_for_input(menu_mouse_pos):
                    button_bling.play()
                    settings()
                if quit_button.check_for_input(menu_mouse_pos):
                    button_bling.play()
                    pg.quit()
                    sys.exit()

        pg.display.update()


def win_screen(winner):
    # Win-screen, der dem Gewinner gratuliert
    global SCREEN
    while True:
        win_screen_mouse_pos = pg.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        win_screen_text1 = get_font(25).render('Congratulations ' + winner, True, '#b68f40')
        win_screen_rect1 = win_screen_text1.get_rect(center=(350, 200))

        win_screen_text2 = get_font(25).render('you won!', True, '#b68f40')
        win_screen_rect2 = win_screen_text2.get_rect(center=(350, 300))

        SCREEN.blit(win_screen_text1, win_screen_rect1)
        SCREEN.blit(win_screen_text2, win_screen_rect2)

        win_screen_back = Button(image=None, pos=(350, 500),
                                 text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green",
                                 rank=0)

        win_screen_back.change_color(win_screen_mouse_pos)
        win_screen_back.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if win_screen_back.check_for_input(win_screen_mouse_pos):
                    button_bling.play()
                    SCREEN = pg.display.set_mode((1280, 720))
                    main_menu()

        pg.display.update()


def draw_screen():
    # Draw-screen, der das Unentschieden mitteilt
    global SCREEN
    while True:
        draw_screen_mouse_pos = pg.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        draw_screen_text = get_font(25).render('It was a Draw!', True, '#b68f40')
        draw_screen_rect = draw_screen_text.get_rect(center=(350, 200))

        SCREEN.blit(draw_screen_text, draw_screen_rect)

        win_screen_back = Button(image=None, pos=(350, 500),
                                 text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green",
                                 rank=0)

        win_screen_back.change_color(draw_screen_mouse_pos)
        win_screen_back.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if win_screen_back.check_for_input(draw_screen_mouse_pos):
                    button_bling.play()
                    SCREEN = pg.display.set_mode((1280, 720))
                    main_menu()

        pg.display.update()


main_menu()
