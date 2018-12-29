from leansim import Worker, Workflow

queue = [Worker(batch_size=1, task_duration=1, pull=False, max_todo=2) for _ in range(4)]
for w1, w2 in zip(queue[:-1], queue[1:]):
    w1.target = w2

queue[2].task_duration = 4
# queue[2].max_todo = 2
workflow = Workflow(workers=queue)
workflow.process(20, verbose=True, sleep_time=0.05)