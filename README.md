# Code Assistant - Screenshot to Code Analyzer

This is a desktop tool that lets you select a region of your screen, take a screenshot, and analyze the contents using OpenAI's GPT-4o vision model. It's designed to help you understand code from images such as terminal outputs, tutorials, or errors.

## Features

- Global hotkey (Shift + A) to trigger screen capture
- Region-based screenshot using a mouse-drag interface
- Sends image to OpenAI for explanation
- Displays both the screenshot and the AI-generated analysis
- Saves the screenshot locally as `img1.png`

## Requirements

- Python 3.8 or higher
- OpenAI API key with GPT-4o access and billing enabled
- Packages:
  - openai
  - python-dotenv
  - pynput
  - PyQt5

Install dependencies:

```bash
pip install openai python-dotenv pynput PyQt5
