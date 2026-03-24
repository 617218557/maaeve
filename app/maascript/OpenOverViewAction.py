from maa.custom_action import CustomAction
from maa.context import Context

# 打开总览
class OpenOverViewAction(CustomAction):
    def run(
            self,
            context: Context,
            argv: CustomAction.RunArg,
    ) -> bool:
        """
        Execute custom action based on image coordinates

        Args:
            context: Task context for executing operations
            argv: Action arguments containing recognition details

        Returns:
            bool: True if action executed successfully
        """
        # Check if recognition found the target
        if argv.reco_detail.hit:
            x, y, w, h = argv.box

            # Check if x-coordinate exceeds threshold
            if x > 1100:
                # Click at position (100, 100)
                context.tasker.controller.post_click(x, y).wait()
                return True
        return False