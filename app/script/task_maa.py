from maa.controller import Controller
from maa.resource import Resource
from maa.tasker import Tasker


def start_maa_task(controller: Controller):
    resource = Resource()
    resource_path = "./assets/resource"
    res_job = resource.post_bundle(resource_path)
    res_job.wait()

    # task
    tasker = Tasker()
    tasker.bind(resource, controller)
    if not tasker.inited:
        print("Failed to init MAA.")
        exit()
    # 起点请在四号谷底区域。
    task_entry = [
        "SettingEntry",
        # "协议空间-打开地图",
        # "制作一个装备",
        # "进行1次简易制作",
        # "提升一次武器等级",
        # "日常活跃度领取",
        # "枢纽区基地电站猫头鹰",
        # "工人之家猫头鹰",
        # "源石研究所猫头鹰",
        # "谷地通道猫头鹰",
        # "矿脉源区医疗站上猫头鹰",
        # "矿脉源区医疗站下猫头鹰",
        # "总控中枢"
    ]
    pipeline_override = {

    }
    for entry in task_entry:
        task_detail = tasker.post_task(entry, pipeline_override).wait().get()
        print(f'task_detail={task_detail}')
        print(f"{entry}执行完成")