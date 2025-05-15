from sentence_transformers import SentenceTransformer
import joblib
from logic.file_loader import get_paragraphs
import pygame

highlight_indices = []
model_path = "models/random_forest_model.pkl"
rf_model = joblib.load(model_path)
sentence_model = SentenceTransformer('cointegrated/rubert-tiny2')

is_processing = False

def run_bert_logic(screen):
    global highlight_indices, is_processing
    paragraphs = get_paragraphs()

    if not paragraphs:
        return

    is_processing = True
    show_loading(screen)

    cleaned = [p for p in paragraphs if len(p.split()) >= 5]
    embeddings = sentence_model.encode(cleaned, show_progress_bar=False)
    predictions = rf_model.predict(embeddings)

    highlight_indices = [i for i, p in enumerate(predictions) if p == 1]
    is_processing = False

def show_loading(screen):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont("timesnewroman", 48)
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((255, 255, 255))
    text = font.render("ИЩУ НЕТОЧНОСТИ", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(overlay, (0, 0))
    screen.blit(text, rect)
    pygame.display.flip()

def get_highlights():
    return highlight_indices

def is_processing_now():
    return is_processing

def reset_state_high():
    global highlight_indices
    highlight_indices = []