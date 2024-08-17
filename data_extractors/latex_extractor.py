"""
Title: LatexExtractorMixed
Author: Trojan
Date: 27-06-2024
"""
import logging
import os
from typing import Any

from PIL import Image

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class LatexExtractor:
    def __init__(self, latex_model_korean: Any, latex_model_japanese: Any, latex_model_chinese: Any):
        self.latex_model_korean = latex_model_korean
        self.latex_model_japanese = latex_model_japanese
        self.latex_model_chinese = latex_model_chinese
        self.models = [self.latex_model_korean, self.latex_model_japanese, self.latex_model_chinese]
        self.downloaded_file_path = os.path.join("downloaded_images", "verification_image.png")

    def recognize_image(self, request_id: str):
        """Recognize text in the given image and optionally save the result."""
        try:
            image = Image.open(self.downloaded_file_path).convert('RGB')
            latex_results = {}
            count = 0
            for model in self.models:
                count += 1
                latex_data = model.recognize_text_formula(image, file_type='text_formula', return_text=False)
                latex_result = model.recognize_text_formula(image, file_type='text_formula')
                total_score = 0
                total_dicts = len(latex_data)
                for data in latex_data:
                    total_score += data["score"]
                final_confidence_score = total_score / total_dicts
                latex_results[f"model_{count}"] = {"text": latex_result, "confidence": final_confidence_score}

            highest_confidence_model = max(latex_results, key=lambda k: latex_results[k]['confidence'])
            highest_confidence = latex_results[highest_confidence_model]['confidence']
            highest_confidence_text = latex_results[highest_confidence_model]['text']

            logging.info(f"Request id : {request_id} -> Extracted Text LatexOCRMixed: {highest_confidence_text}")
        except Exception as e:
            logging.error(f"Request id : {request_id} -> Error with exception: {e}")
            return f"error: {str(e)}"
        return highest_confidence_text, highest_confidence
