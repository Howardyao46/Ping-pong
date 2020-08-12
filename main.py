#Warning: "Complete Challenge" level is super glitchy. We recommend you not to play that.

import pygame as pg

red = (255, 0, 0)
dark_red = (128, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
golden = (128, 128, 0)
green = (0, 255, 0)
dark_green = (0, 128, 0)
blue = (0, 0, 255)
indigo = (0, 0, 128)
cyan = (0, 255, 255)
purple = (128, 0, 255)
magenta = (255, 0, 255)
white = (255, 255, 255)
grey = (128, 128, 128)
brown = (105, 60, 42)
black = (0, 0, 0)

startx = 111
starty = 10
start_paddle_x = 100
start_paddle_y = 250
rightx = True
downy = True
speed = 1


def create_graphics_screen():
    global FONT
    pg.init()
    screen = pg.display.set_mode((800, 580))
    pg.display.set_caption('Ping Pong in Pygame')
    FONT = pg.font.Font(None, 32)
    return screen


def select_events():
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.KEYUP, pg.KEYDOWN])


def display_first_screen(screen):
    global score_box
    pg.draw.rect(screen, cyan, (start_paddle_x, start_paddle_y, 10, 100), 0)
    print(startx, starty)
    pg.draw.circle(screen, orange, (startx, starty), 10, 0)
    score_box = LabelBox(500, 480, 140, 100, "You: 0", "Computer: 0")
    pg.display.update()


def draw_circle(screen):
    global startx, starty, rightx, downy
    global start_paddle_x, start_paddle_y

    human_win = False
    comp_win = False
    pg.draw.circle(screen, black, (startx, starty), 10, 0)
    randx = 3
    randy = 3

    if rightx:
        if startx + randx < 750:
            startx = startx + randx
        else:
            startx = startx - randx
            rightx = False
    else:
        if startx - start_paddle_x < (
                randx + 10) and starty > start_paddle_y and starty < (
                    start_paddle_y + 100):
            startx = startx + randx
            rightx = True
            human_win = True
        else:
            if startx - randx > 50:
                startx = startx - randx
            else:
                startx = startx + randx
                rightx = True
                comp_win = True

    if downy:
        if starty + randy < 520:
            starty = starty + randy
        else:
            starty = starty - randy
            downy = False
    else:
        if starty - randy > 30:
            starty = starty - randy
        else:
            starty = starty + randy
            downy = True

    pg.draw.circle(screen, orange, (startx, starty), 10, 0)
    return (human_win, comp_win)


def main_loop(screen):
    global start_paddle_x, start_paddle_y, speed
    human_score = 0
    comp_score = 0
    done = False

    print("speed =", speed)
    while not done:
        #   This for loop moves the paddle
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                done = True
            if ev.type == pg.KEYDOWN:
                pg.draw.rect(screen, black,
                             (start_paddle_x, start_paddle_y, 10, 100), 0)
                if ev.scancode == 98:
                    start_paddle_y = start_paddle_y - 50
                if ev.scancode == 104:
                    start_paddle_y = start_paddle_y + 50
                pg.draw.rect(screen, cyan,
                             (start_paddle_x, start_paddle_y, 10, 100), 0)


# This part moves the ball
        (human_win, comp_win) = draw_circle(screen)
        print(startx, starty)

        # Now we update the score
        if human_win:
            human_score = human_score + 1
        elif comp_win:
            comp_score = comp_score + 1
        score_box.update_text("You: " + str(human_score),
                              "Computer: " + str(comp_score))
        if human_score == 10:
            winner = LabelBox(300, 280, 140, 32, "You Win !!", "")
            done = True
        elif comp_score == 10:
            winner = LabelBox(300, 280, 140, 32, "Computer Won !!", "")
            done = True
        if done:
            pg.display.update()
            click = False
            while not click:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        click = True

        pg.display.update()
        pg.time.delay(20 - speed)


class Button:
    def __init__(self, x, y, w, h, level):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('dodgerblue2')
        self.level = level
        if level == "Complete Challenge":
            text = "Complete Challenge"
        elif level == "6":
            text = "6"
        elif level == "5":
            text = "5"
        elif level == "4":
            text = "4"
        elif level == "3":
            text = "3"
        elif level == "2 (recommended)":
            text = "2 (recommended)"
        elif level == "1":
            text = "1"
        self.txt_surface = FONT.render(text, True, self.color)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    def get_level(self):
        return self.level

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                return True

    def update_text(self, text):
        self.txt_surface = FONT.render(text, True, self.color)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class LabelBox:
    def __init__(self, x, y, w, h, text1, text2):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('dodgerblue2')
        self.txt_surface = FONT.render(text1, True, self.color)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.text1 = text1
        self.text2 = text2
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        self.txt_surface2 = FONT.render(text2, True, self.color)
        width = max(200, self.txt_surface2.get_width() + 10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface2, (self.rect.x + 5, self.rect.y + 45))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    def update_text(self, text1, text2):
        mask_txt_surface = FONT.render(self.text1, True, pg.Color('black'))
        # Blit the text.
        screen.blit(mask_txt_surface, (self.rect.x + 5, self.rect.y + 5))

        self.text1 = text1
        self.txt_surface = FONT.render(text1, True, self.color)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        mask_txt_surface2 = FONT.render(self.text2, True, pg.Color('black'))
        # Blit the text.
        screen.blit(mask_txt_surface2, (self.rect.x + 5, self.rect.y + 45))

        self.text2 = text2
        self.txt_surface2 = FONT.render(text2, True, self.color)
        width = max(200, self.txt_surface2.get_width() + 10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface2, (self.rect.x + 5, self.rect.y + 45))
        pg.draw.rect(screen, self.color, self.rect, 2)


def textbox():
    global speed
    clock = pg.time.Clock()
    input_box1 = Button(100, 180, 140, 32, "1")
    input_box2 = Button(100, 230, 140, 32, "2 (recommended)")
    input_box3 = Button(100, 280, 140, 32, "3")
    input_box4 = Button(100, 330, 140, 32, "4")
    input_box5 = Button(100, 380, 140, 32, "5")
    input_box6 = Button(100, 430, 140, 32, "6")
    input_box7 = Button(100, 480, 140, 32, "Complete Challenge")
    input_boxes = [
        input_box1, input_box2, input_box3, input_box4, input_box5, input_box6,
        input_box7
    ]
    done = False
    pg.display.flip()

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                if box.handle_event(event):
                    gl = box.get_level()
                    if gl == "Complete Challenge":
                        speed = 20
                    elif gl == "6":
                        speed = 18
                    elif gl == "5":
                        speed = 16
                    elif gl == "4":
                        speed = 14
                    elif gl == "3":
                        speed = 12
                    elif gl == "2 (recommended)":
                        speed = 10
                    elif gl == "1":
                        speed = 8
                    screen.fill(pg.Color('black'))
                    done = True
        clock.tick(30)
    print(speed)
    pg.display.update()


if __name__ == '__main__':
    screen = create_graphics_screen()
    textbox()
    select_events()
    display_first_screen(screen)
    main_loop(screen)
    pg.quit()
