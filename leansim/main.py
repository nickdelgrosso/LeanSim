import argparse
from . import Worker, Workflow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', '-w', default=4, help='Number of workers in value stream.')
    parser.add_argument('--work', default=20, help='Number of products to make.')
    parser.add_argument('--duration', default=2, help='Number of time steps each process takes.')
    parser.add_argument('--batch', default=20, help='Batch size for each worker.')
    parser.add_argument('--sleep', default=0.2, help='Time to sleep between steps.')
    # parser.add_argument('--bottleneck', default=False)

    args = parser.parse_args()
    Workflow.run_chained_process(workers=args.workers, work=args.work, task_duration=args.duration, batch_size=args.batch,
                                 verbose=True, sleep_time=args.sleep)



if __name__ == '__main__':
    main()

#
#
#
# queue = [Worker(batch_size=1, task_duration=2, capacity=1, pull=True, max_todo=2) for _ in range(4)]
# for w1, w2 in zip(queue[:-1], queue[1:]):
#     w1.target = w2
#
# queue[2].task_duration = 10
# queue[2].capacity = 4
# queue[2].max_todo = 10
# workflow = Workflow(workers=queue)
# workflow.process(100, verbose=True, sleep_time=0.1)