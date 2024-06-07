import pygame

from source.draw.rectangle import draw_dashed_rounded_rectangle


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))  # Fill the screen with black
        draw_dashed_rounded_rectangle(screen, (255, 255, 255), (
            100, 100, 500, 300), 1, 15, 5)  # Draw a dashed rounded rectangle

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
