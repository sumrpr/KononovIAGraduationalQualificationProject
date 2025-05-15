import pygame
from logic.file_loader import get_paragraphs
from logic.analyzer import get_highlights

font = pygame.font.SysFont("timesnewroman", 24)
button_images = {}
button_rects = {}
WIDTH, HEIGHT = 1920, 1000
BUTTON_BAR_HEIGHT = 400
PARAGRAPH_SPACING = 20
FONT_SIZE = 24

def setup_ui(width, height):
    global button_images, button_rects, WIDTH, HEIGHT
    WIDTH, HEIGHT = width, height
    button_images["open"] = pygame.image.load("assets/Open.png")
    button_images["run"] = pygame.image.load("assets/Play.png")
    button_images["reset"] = pygame.image.load("assets/Reset.png")

    button_rects["open"] = button_images["open"].get_rect(topleft=(60, 20))
    button_rects["run"] = button_images["run"].get_rect(topleft=(800, 20))
    button_rects["reset"] = button_images["reset"].get_rect(topleft=(1500, 20))

def get_button_rects():
    return button_rects

def draw_buttons(screen):
    for key in button_images:
        screen.blit(button_images[key], button_rects[key])

def draw_text(screen, scroll_offset):
    x = 50
    y = BUTTON_BAR_HEIGHT + scroll_offset
    paragraphs = get_paragraphs()
    highlights = get_highlights()

    for i, para in enumerate(paragraphs):
        lines = wrap_text(para, WIDTH - 100)
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255) if i in highlights else (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(x, y))
            if text_rect.bottom > BUTTON_BAR_HEIGHT and text_rect.top < HEIGHT:
                if i in highlights:
                    pygame.draw.rect(screen, (255, 100, 100), text_rect.inflate(10, 10))
                screen.blit(text_surface, text_rect)
            y += FONT_SIZE + 5
        y += PARAGRAPH_SPACING

def wrap_text(text, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines