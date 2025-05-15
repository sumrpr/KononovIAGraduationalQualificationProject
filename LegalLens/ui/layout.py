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

def draw_scrollbar(screen, scroll_offset):
    paragraphs = get_paragraphs()
    total_height = 0
    for para in paragraphs:
        total_height += len(wrap_text(para, WIDTH - 100)) * (FONT_SIZE + 5) + PARAGRAPH_SPACING

    visible_height = HEIGHT - BUTTON_BAR_HEIGHT
    if total_height <= visible_height:
        return

    scrollbar_width = 10
    scrollbar_height = int((visible_height / total_height) * visible_height)
    scrollbar_x = WIDTH - 20
    scroll_max = -(total_height - visible_height)
    scroll_ratio = scroll_offset / scroll_max if scroll_max != 0 else 0
    scrollbar_y = BUTTON_BAR_HEIGHT + int((visible_height - scrollbar_height) * scroll_ratio)

    pygame.draw.rect(screen, (200, 200, 200), (scrollbar_x, BUTTON_BAR_HEIGHT, scrollbar_width, visible_height))
    pygame.draw.rect(screen, (100, 100, 100), (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))

def handle_drag_scrollbar(mouse_y, drag_offset_y, current_scroll_offset):
    paragraphs = get_paragraphs()
    total_height = 0
    for para in paragraphs:
        total_height += len(wrap_text(para, WIDTH - 100)) * (FONT_SIZE + 5) + PARAGRAPH_SPACING

    visible_height = HEIGHT - BUTTON_BAR_HEIGHT
    scroll_area_height = visible_height - int((visible_height / total_height) * visible_height)
    new_y = max(BUTTON_BAR_HEIGHT, min(mouse_y - drag_offset_y, BUTTON_BAR_HEIGHT + scroll_area_height))
    scroll_ratio = (new_y - BUTTON_BAR_HEIGHT) / scroll_area_height
    new_offset = -int((total_height - visible_height) * scroll_ratio)
    return new_offset

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
