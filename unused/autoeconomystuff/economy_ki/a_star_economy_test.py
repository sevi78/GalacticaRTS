import pygame
import sys
from source.handlers.file_handler import load_file

buildings = load_file("buildings.json", "config")

def initialize_pygame():
    pygame.init()
    width, height = 400, 300
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simple Pygame App")
    return screen, width, height

def create_text(message, font_size, color, width, height):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(width/2, height/2))
    return text, text_rect

def main_loop(screen, text, text_rect):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()

def cleanup():
    pygame.quit()
    sys.exit()

def main():
    screen, width, height = initialize_pygame()
    text, text_rect = create_text("test", 36, (255, 255, 255), width, height)
    main_loop(screen, text, text_rect)
    cleanup()

if __name__ == "__main__":
    main()

