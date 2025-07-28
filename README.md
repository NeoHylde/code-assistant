# Code Assistant: Screenshot to Code Analyzer

A desktop tool that lets you select a screen region, take a screenshot, and analyze it using OpenAI's GPT-4o Vision model. Useful for understanding terminal outputs, tutorial snippets, or debugging screenshots.

## Features

- Trigger capture from anywhere using a global hotkey (Shift + A)
- Draw a selection box with your mouse to capture a specific screen region
- Screenshot is automatically analyzed with GPT-4o
- Displays both the captured image and GPT-generated explanation
- Image is saved locally as `img1.png`
- Includes a workaround to ensure Escape key works on initial capture

## Requirements

- Python 3.8 or newer
- OpenAI API key with GPT-4o access and billing enabled
- Dependencies:
  - openai
  - python-dotenv
  - pynput
  - PyQt5
  - mouse
  - Pillow

Install everything with:

```bash
pip install openai python-dotenv pynput PyQt5 mouse Pillow