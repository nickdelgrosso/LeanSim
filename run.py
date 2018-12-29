from leansim import Worker, Workflow

queue = [Worker(batch_size=1, task_duration=2, capacity=1, pull=True, max_todo=2) for _ in range(4)]
for w1, w2 in zip(queue[:-1], queue[1:]):
    w1.target = w2

queue[2].task_duration = 10
queue[2].capacity = 4
queue[2].max_todo = 10
workflow = Workflow(workers=queue)
workflow.process(100, verbose=True, sleep_time=0.1)