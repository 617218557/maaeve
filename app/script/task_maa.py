import logging

from maa.controller import Controller
from maa.tasker import Tasker

# 获取 logger
logger = logging.getLogger()


def start_maa_task(controller: Controller, tasker: Tasker):
    task_entry = [
        "开始",
    ]
    pipeline_override = {

    }
    for entry in task_entry:
        task_detail = tasker.post_task(entry, pipeline_override).wait().get()
        logger.info(f'task_detail={task_detail}')
        logger.info(f"{entry}执行完成")