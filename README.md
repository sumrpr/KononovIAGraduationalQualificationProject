# ВКР Кононова Ильи Александровича
Репозиторий для выпускной квалификационной работы Кононова Ильи Александровича

Legal Lens – инструмент для проверки документов в рамках Due Diligence

# LegalLens — Поиск неточностей в юридических документах

LegalLens — это десктопное приложение на Python, позволяющее загружать юридические документы в форматах .txt, .docx и .pdf и находить потенциальные неточности при помощи моделей машинного обучения.

## Основные возможности

- Загрузка документов через графический интерфейс
- Поддержка .txt, .docx и .pdf
- Обработка текста с помощью Sentence-BERT и Random Forest
- Подсветка подозрительных абзацев
- Кнопки:
  - Открыть документ
  - Запустить анализ
  - Сбросить

## Установка

1. Убедитесь, что у вас установлен Python 3.10+
2. Установите зависимости:

```bash
pip install -r requirements.txt
```
Убедитесь, что у вас есть файл модели:

random_forest_model.pkl должен находиться в корне проекта.

Запустите приложение: 
```bash
python main.py
```
## Структура проекта:
```bash
LegalLens/
├── assets/                         # Графические ресурсы для интерфейса
│   ├── Open.png
│   ├── Play.png
│   └── Reset.png
│
├── logic/                          # Логика приложения
│   ├── analyzer.py                 # Обработка моделью и логика подсветки
│   └── file_loader.py             # Загрузка, хранение и сброс текста
│
├── models/                         # Модель
│   └── random_forest_model.pkl
│
├── ui/                             # Отображение интерфейса
│   └── layout.py                  # Рендер текста и кнопок
│
├── main.py                         # Главный файл запуска интерфейса
└── requirements.txt                # Список зависимостей проекта
```

## Для реализации проекта были использованы следующие технические решения:

1. Random Forest для обучения и выполнения поиска некорректных пунктов. Была выбрана именно эта модель, 
так как она хорошо справляется с бинарной классификаицей, при это может работать крайне быстро

2. RuBERT для задачи токенизации и эмбединга датасета при обучении. Была выбрана версия модели BERT, 
предобученная на русских текстах, так как сама по себе BERT хорошо справляется с глубоким пониманием текста,
а тот факт, что она уже была предобучена на русских текстах, позволяет её лучше ориентироваться в 
локальных нормативных актах, написанных на рууском языке.

3. API GigaChat для задачи разметки текста в датасете. Был выбран из-за доступности API, а так же высоких
результатов, демонстрируемых данной большой языковой моделью

4. Pygame для создания интерфейса. Данная библиотека была выбрана, так как она дает достаточно свободы для
размешения собственного дизайна, не привязана к сторонним приложениям и решениям, проста в обращении.

