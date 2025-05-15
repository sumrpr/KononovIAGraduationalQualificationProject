import pygame
pygame.init()

from ui.layout import draw_buttons, draw_text
from logic.file_loader import open_file_dialog, load_file, reset_state_para
from logic.analyzer import run_bert_logic, reset_state_high, is_processing

import sys


WIDTH, HEIGHT = 1920, 1000
BUTTON_BAR_HEIGHT = 400
SCROLL_SPEED = 160

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legal Lens")
clock = pygame.time.Clock()

scroll_offset = 0

from ui.layout import setup_ui, get_button_rects
setup_ui(WIDTH, HEIGHT)

button_rects = get_button_rects()

running = True
while running:
    screen.fill((245, 245, 245))
    draw_buttons(screen)
    draw_text(screen, scroll_offset)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                scroll_offset = min(scroll_offset + SCROLL_SPEED, 0)
            elif event.y < 0:
                scroll_offset -= SCROLL_SPEED

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if button_rects["open"].collidepoint(mouse_pos):
                filepath = open_file_dialog()
                if filepath:
                    load_file(filepath)
                    scroll_offset = 0

            elif button_rects["run"].collidepoint(mouse_pos):
                run_bert_logic(screen)

            elif button_rects["reset"].collidepoint(mouse_pos):
                reset_state_high()
                reset_state_para()
                scroll_offset = 0


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()