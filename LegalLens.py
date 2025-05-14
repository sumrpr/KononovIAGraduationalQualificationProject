import pygame
import os
import sys
import docx
import pdfplumber
import tkinter as tk
from tkinter import filedialog
from sentence_transformers import SentenceTransformer
import joblib
import numpy as np

# Initialize tkinter for file dialogs
root = tk.Tk()
root.withdraw()

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 1920, 1000  # Обновим размеры окна
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
BG_COLOR = (245, 245, 245)

FONT_SIZE = 24
PARAGRAPH_SPACING = 20
BUTTON_BAR_HEIGHT = 400  # Height for the button strip at the top

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legal Lens")
font = pygame.font.SysFont("timesnewroman", FONT_SIZE)

clock = pygame.time.Clock()
scroll_offset = 0
SCROLL_SPEED = 160

# Load button images
button_images = {
    "open": pygame.image.load("Open.png"),
    "run": pygame.image.load("Play.png"),
    "reset": pygame.image.load("Reset.png")
}
button_rects = {
    "open": button_images["open"].get_rect(topleft=(60, 20)),
    "run": button_images["run"].get_rect(topleft=(800, 20)),
    "reset": button_images["reset"].get_rect(topleft=(1500, 20))
}

# Globals
paragraphs = []
highlight_indices = []
model_path = "random_forest_model.pkl"
rf_model = joblib.load(model_path)
sentence_model = SentenceTransformer('cointegrated/rubert-tiny2')
is_dragging_scrollbar = False
scrollbar_rect = pygame.Rect(0, 0, 0, 0)
is_processing = False  # Показываем "ИЩУ НЕТОЧНОСТИ"

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Supported Files", "*.txt *.docx *.pdf"), ("All Files", "*.*")])
    return file_path

def load_file(filepath):
    global paragraphs
    ext = filepath.split(".")[-1].lower()
    text = ""
    try:
        if ext == "txt":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext == "docx":
            doc = docx.Document(filepath)
            text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == "pdf":
            with pdfplumber.open(filepath) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                text = "\n\n".join(p.strip() for p in pages if p.strip())
    except Exception as e:
        print(f"Error reading file: {e}")
        text = ""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

def run_bert_logic():
    global highlight_indices, is_processing

    if not paragraphs:
        return

    is_processing = True
    pygame.display.flip()  # Обновим экран перед началом

    # Показать "ИЩУ НЕТОЧНОСТИ"
    overlay = pygame.Surface((WIDTH, HEIGHT - BUTTON_BAR_HEIGHT))
    overlay.fill(WHITE)
    screen.blit(overlay, (0, BUTTON_BAR_HEIGHT))

    loading_font = pygame.font.SysFont("timesnewroman", 48)
    loading_text = loading_font.render("ИЩУ НЕТОЧНОСТИ", True, BLACK)
    loading_rect = loading_text.get_rect(center=(WIDTH // 2, (HEIGHT + BUTTON_BAR_HEIGHT) // 2))
    screen.blit(loading_text, loading_rect)

    pygame.display.flip()

    # Выполнить модель
    cleanedParas = paragraphs
    for i in cleanedParas:
        il = i.split(' ')
        if len(il) < 5:
            cleanedParas.pop(cleanedParas.index(i))

    embeddings = sentence_model.encode(cleanedParas, show_progress_bar=False)
    predictions = rf_model.predict(embeddings)
    highlight_indices = [i for i, pred in enumerate(predictions) if pred == 1]

    is_processing = False  

def reset():
    global paragraphs, highlight_indices
    paragraphs = []
    highlight_indices = []

def draw_buttons():
    # Draw the buttons in the reserved space at the top
    for key in button_images:
        screen.blit(button_images[key], button_rects[key])

def draw_text():
    # Start drawing the text below the button bar (BUTTON_BAR_HEIGHT)
    y = BUTTON_BAR_HEIGHT + scroll_offset
    x = 50  # Padding from the left side of the screen
    for i, para in enumerate(paragraphs):
        lines = wrap_text(para, WIDTH - 100, font)
        for line in lines:
            text_surface = font.render(line, True, WHITE if i in highlight_indices else BLACK)
            text_rect = text_surface.get_rect(topleft=(x, y))
            if text_rect.bottom > BUTTON_BAR_HEIGHT and text_rect.top < HEIGHT:  # Only draw if visible
                if i in highlight_indices:
                    pygame.draw.rect(screen, RED, text_rect.inflate(10, 10))
                screen.blit(text_surface, text_rect)
            y += FONT_SIZE + 5
        y += PARAGRAPH_SPACING

def wrap_text(text, max_width, font):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        line_width = font.size(test_line)[0]
        
        if line_width <= max_width:
            current_line = test_line
        else:
            # If the word doesn't fit, append the current line and start a new one
            lines.append(current_line)
            current_line = word
            
    if current_line:  # Add the last line
        lines.append(current_line)
    
    return lines

def draw_scrollbar():
    global scrollbar_rect
    total_height = 0
    for para in paragraphs:
        lines = wrap_text(para, WIDTH - 100, font)
        total_height += len(lines) * (FONT_SIZE + 5) + PARAGRAPH_SPACING

    visible_height = HEIGHT - BUTTON_BAR_HEIGHT
    if total_height <= visible_height:
        scrollbar_rect = pygame.Rect(0, 0, 0, 0)
        return

    scrollbar_width = 10
    scrollbar_height = int((visible_height / total_height) * visible_height)
    scrollbar_x = WIDTH - 20
    scroll_max = -(total_height - visible_height)
    scroll_ratio = scroll_offset / scroll_max if scroll_max != 0 else 0
    scrollbar_y = BUTTON_BAR_HEIGHT + int((visible_height - scrollbar_height) * scroll_ratio)

    scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)

    pygame.draw.rect(screen, (200, 200, 200), (scrollbar_x, BUTTON_BAR_HEIGHT, scrollbar_width, visible_height))
    pygame.draw.rect(screen, (100, 100, 100), scrollbar_rect)

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_buttons()
    draw_text()
    draw_scrollbar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse wheel scrolling (MOUSEWHEEL event)
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scroll up
                scroll_offset = min(scroll_offset + SCROLL_SPEED, 0)
            elif event.y < 0:  # Scroll down
                scroll_offset -= SCROLL_SPEED

        # Handle mouse button clicks (only left-click)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Only handle left-click (button 1)
                mouse_pos = pygame.mouse.get_pos()
                if button_rects["open"].collidepoint(mouse_pos):
                    filepath = open_file_dialog()
                    if filepath:
                        load_file(filepath)
                        scroll_offset = 0
                elif button_rects["run"].collidepoint(mouse_pos):
                    run_bert_logic()
                elif button_rects["reset"].collidepoint(mouse_pos):
                    reset()
                    scroll_offset = 0

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                scroll_offset = min(scroll_offset + SCROLL_SPEED, 0)
            elif event.key == pygame.K_DOWN:
                scroll_offset -= SCROLL_SPEED
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if scrollbar_rect.collidepoint(mouse_pos):
                    is_dragging_scrollbar = True
                    drag_offset_y = mouse_pos[1] - scrollbar_rect.y
                # Кнопки:
                elif button_rects["open"].collidepoint(mouse_pos):
                    filepath = open_file_dialog()
                    if filepath:
                        load_file(filepath)
                        scroll_offset = 0
                elif button_rects["run"].collidepoint(mouse_pos):
                    run_bert_logic()
                elif button_rects["reset"].collidepoint(mouse_pos):
                    reset()
                    scroll_offset = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION and is_dragging_scrollbar:
            total_height = 0
            for para in paragraphs:
                lines = wrap_text(para, WIDTH - 100, font)
                total_height += len(lines) * (FONT_SIZE + 5) + PARAGRAPH_SPACING

            visible_height = HEIGHT - BUTTON_BAR_HEIGHT
            scroll_area_height = visible_height - scrollbar_rect.height
            if scroll_area_height > 0:
                mouse_y = event.pos[1]
                new_y = max(BUTTON_BAR_HEIGHT, min(mouse_y - drag_offset_y, BUTTON_BAR_HEIGHT + scroll_area_height))
                scroll_ratio = (new_y - BUTTON_BAR_HEIGHT) / scroll_area_height
                scroll_offset = -int((total_height - visible_height) * scroll_ratio)
    if is_processing:
        overlay = pygame.Surface((WIDTH, HEIGHT - BUTTON_BAR_HEIGHT))
        overlay.fill(WHITE)
        screen.blit(overlay, (0, BUTTON_BAR_HEIGHT))
        loading_font = pygame.font.SysFont("timesnewroman", 48)
        loading_text = loading_font.render("ИЩУ НЕТОЧНОСТИ", True, BLACK)
        loading_rect = loading_text.get_rect(center=(WIDTH // 2, (HEIGHT + BUTTON_BAR_HEIGHT) // 2))
        screen.blit(loading_text, loading_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
