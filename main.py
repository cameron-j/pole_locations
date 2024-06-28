import pygame

LINE_COL = "black"
BACKGROUND_COL = "white"
POLE_COL = "red"

LEFT_BOUND = -2
RIGHT_BOUND = 2
DOWN_BOUND = -2
UP_BOUND = 2

X_TICK_INTERVAL = 0.1
X_LABEL_INTERVAL = 0.5
Y_TICK_INTERVAL = 0.1
Y_LABEL_INTERVAL = 0.5
MINOR_TICK_HEIGHT = 8
MAJOR_TICK_HEIGHT = 50

CROSS_SIZE = 16

INPUT_WIN_WIDTH = 500
INPUT_WIN_HEIGHT = 500

pygame.init()

input_win = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

def screen_to_coord(pos):
    return ((pos[0] - INPUT_WIN_WIDTH / 2) * (RIGHT_BOUND - LEFT_BOUND) / INPUT_WIN_WIDTH,
            (INPUT_WIN_HEIGHT / 2 - pos[1]) * (UP_BOUND - DOWN_BOUND) / INPUT_WIN_HEIGHT)

def coord_to_screen(pos):
    return ((pos[0] * INPUT_WIN_WIDTH / (RIGHT_BOUND - LEFT_BOUND)) + INPUT_WIN_WIDTH / 2,
            INPUT_WIN_HEIGHT / 2 - (pos[1] * INPUT_WIN_HEIGHT / (UP_BOUND - DOWN_BOUND)))

def draw_cross(surface, pos):
    pygame.draw.line(surface, POLE_COL, (pos[0] - CROSS_SIZE / 2, pos[1] - CROSS_SIZE / 2),
                     (pos[0] + CROSS_SIZE / 2, pos[1] + CROSS_SIZE / 2))
    pygame.draw.line(surface, POLE_COL, (pos[0] - CROSS_SIZE / 2, pos[1] + CROSS_SIZE / 2),
                     (pos[0] + CROSS_SIZE / 2, pos[1] - CROSS_SIZE / 2))

def main():
    poles = [(0, 0)]
    n_poles = 0

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEMOTION:
                # Update the graph to show the new position of the pole
                poles[n_poles] = screen_to_coord(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Add the current mouse position to poles
                poles.append(screen_to_coord(pygame.mouse.get_pos()))
                n_poles += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    poles = [screen_to_coord(pygame.mouse.get_pos())]
                    n_poles = 0

        # Draw the coordinate axes
        input_win.fill(BACKGROUND_COL)
        pygame.draw.line(input_win, LINE_COL, (0, INPUT_WIN_HEIGHT / 2), (INPUT_WIN_WIDTH, INPUT_WIN_HEIGHT / 2))
        pygame.draw.line(input_win, LINE_COL, (INPUT_WIN_WIDTH / 2, 0), (INPUT_WIN_WIDTH / 2, INPUT_WIN_HEIGHT))

        # Unit circle
        uc_bottom_left = coord_to_screen((-1, -1))
        uc_top_right = coord_to_screen((1, 1))
        uc_rect = pygame.Rect(uc_bottom_left[0], uc_top_right[1], uc_top_right[0] - uc_bottom_left[0], uc_bottom_left[1] - uc_top_right[1])
        pygame.draw.ellipse(input_win, LINE_COL, uc_rect, width=1)

        # Axis ticks
        x = LEFT_BOUND
        while x <= RIGHT_BOUND:
            tick_loc = coord_to_screen((x, 0))
            pygame.draw.line(input_win, LINE_COL, (tick_loc[0], tick_loc[1] - MINOR_TICK_HEIGHT / 2),
                            (tick_loc[0], tick_loc[1] + MINOR_TICK_HEIGHT / 2))
            x += X_TICK_INTERVAL

        y = DOWN_BOUND
        while y <= UP_BOUND:
            tick_loc = coord_to_screen((0, y))
            pygame.draw.line(input_win, LINE_COL, (tick_loc[0] - MINOR_TICK_HEIGHT / 2, tick_loc[1]),
                            (tick_loc[0] + MINOR_TICK_HEIGHT / 2, tick_loc[1]))
            y += Y_TICK_INTERVAL

        # Existing pole locations
        for pole in poles:
            draw_cross(input_win, coord_to_screen(pole))

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
