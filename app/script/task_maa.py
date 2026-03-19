from maa.controller import Controller
from maa.tasker import Tasker


def start_maa_task(controller: Controller, tasker: Tasker):
    task_entry = [
        "SettingEntry",
    ]
    pipeline_override = {

    }
    for entry in task_entry:
        task_detail = tasker.post_task(entry, pipeline_override).wait().get()
        print(f'task_detail={task_detail}')
        print(f"{entry}执行完成")