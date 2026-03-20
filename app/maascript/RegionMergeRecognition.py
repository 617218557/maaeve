from maa.custom_recognition import CustomRecognition
from maa.context import Context
import numpy as np


class RegionMergeRecognition(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg):
        # 获取之前And识别的结果
        and_result = context.run_recognition("FindThreeImages", argv.image)
        if not and_result or not and_result.hit:
            return None

            # 从And识别结果中提取3个子区域
        detail = and_result.best_result.sub_results
        if not isinstance(detail, list) or len(detail) < 3:
            return None

            # 获取3个区域的坐标
        boxes = []
        for sub_result in detail[:3]:
            if sub_result.best_result.box is not None:
                boxes.append(sub_result.best_result.box)

        if len(boxes) != 3:
            return None

            # 计算合并区域的最小外接矩形
        min_x = min(box[0] for box in boxes)
        min_y = min(box[1] for box in boxes)
        max_x = max(box[0] + box[2] for box in boxes)
        max_y = max(box[1] + box[3] for box in boxes)

        merged_box = (min_x, min_y, max_x - min_x, max_y - min_y)

        return CustomRecognition.AnalyzeResult(
            box=merged_box,
            detail={
                "merged_box": merged_box,
                "original_boxes": boxes
            }
        )