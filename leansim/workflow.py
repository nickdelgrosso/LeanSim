from time import sleep
import os
from .worker import Worker


class Workflow:
    
    def __init__(self, workers):
        self.workers = workers
        self.work_done = 0

    @property
    def total_work(self):
        return sum(w.wip + w.done for w in self.workers)

    @property
    def wip(self):
        return self.total_work - self.workers[0].todo
        
    def step(self):
        for worker in self.workers[::-1]:
            work_done = worker.work()
            worker.push()
            self.work_done += work_done

    def process(self, work, verbose=False, sleep_time=0):
        """Returns number of steps to process some piece of work."""
        self.workers[0].todo = work
        steps = 0
        while self.total_work:
            steps += 1
            self.step()
            if verbose:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self)
                print(f'Steps: {steps}', end='\n\n', flush=True)
                if sleep_time:
                    sleep(sleep_time)
        return steps

    def __repr__(self):
        rep = ''
        for attr in ['task_duration', 'capacity', 'batch_size', 'max_todo', '', 'todo', 'doing', 'done', '', 'wip']:
            rep += '{:>15}:'.format(attr)
            for w in self.workers:
                if attr:
                    val = getattr(w, attr)
                    val = len(val) if hasattr(val, '__iter__') else val
                    rep += '\t {}'.format(val if val else ' ')
                else:
                    rep += '\t---'
            rep += '\n'

        rep += '-----------------------------------------------------------\n'

        for attr in ['total_work', 'wip', 'work_done']:
            rep += '{}: {}     '.format(attr, getattr(self, attr))

        return rep
    
    @classmethod
    def run_chained_process(cls, work=20, workers=4, verbose=False, sleep_time=0.2, **worker_kwargs):
        queue = [Worker(**worker_kwargs) for _ in range(workers)]
        for w1, w2 in zip(queue[:-1], queue[1:]):
            w1.target = w2
        
        workflow = cls(workers=queue)
        steps = workflow.process(work=work, verbose=verbose, sleep_time=sleep_time)
        return steps