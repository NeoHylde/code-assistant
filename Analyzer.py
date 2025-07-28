import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class AnalyzerWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.file_path = file_path

    def run(self):
        try:
            client = OpenAI(api_key=self.api_key)

            #Encode img
            with open(self.file_path, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode("utf-8")

            #Send img to gpt api, get response
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Briefly explain the logic in this code."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
            )

            #store result
            result = response.choices[0].message.content
            self.finished.emit(result)
        
        except Exception as e:
            self.error.emit(str(e))
