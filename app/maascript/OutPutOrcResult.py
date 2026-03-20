from maa.custom_recognition import CustomRecognition
from maa.context import Context
import numpy as np

class PrintOrcResult(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg):
        # 获取之前And识别的结果
        and_result = context.run_recognition("OCROnMerged", argv.image)

        return CustomRecognition.AnalyzeResult(
            box=None,
            detail={
                "merged_box": "",
                "original_boxes": ""
            }
        )