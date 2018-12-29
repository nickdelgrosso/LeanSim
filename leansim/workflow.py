from IPython.display import clear_output
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
            worker.push()
            work_done = worker.work()
            self.work_done += work_done

    def process(self, work, verbose=False, sleep_time=0):
        """Returns number of steps to process some piece of work."""
        self.workers[0].todo = work
        steps = 0
        while self.total_work:
            steps += 1
            self.step()
            if verbose:
                clear_output()
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self)
                print(f'Steps: {steps}', end='\n\n', flush=True)
                if sleep_time:
                    sleep(sleep_time)
        return steps
    
    def __repr__(self):
        rep = ''

        rep += 'pull:\t ' + '\t '.join('Y' if w.pull else ' ' for w in self.workers) + '\n'
        rep += 'task:\t ' + '\t '.join(str(w.task_duration) if w.task_duration > 1 else ' ' for w in self.workers) + '\n'
        rep += 'capaci:\t ' + '\t '.join(str(w.capacity) if w.capacity > 1 else ' ' for w in self.workers) + '\n'
        rep += 'batch:\t ' + '\t '.join(str(w.batch_size) if w.batch_size > 1 else ' ' for w in self.workers) + '\n'
        rep += 'limit:\t ' + '\t '.join(str(w.max_todo) if w.max_todo else ' ' for w in self.workers) + '\n'

        rep += ''.join('\t---' for _ in self.workers) + '\n'

        # for idx, w in enumerate(self.workers):
        #     rep += f'\t-'
        # rep += '\n'
        rep += f'todo:\t ' + '\t '.join(f'{w.todo if w.todo else " "}' for w in self.workers) + '\n'
        rep += f'doing:\t ' + '\t '.join(f'{len(w.doing) if w.doing else " "}' for w in self.workers) + '\n'
        rep += f'done:\t ' + '\t '.join(f'{w.done if w.done else " "}' for w in self.workers) + '\n'

        rep += ''.join('\t---' for _ in self.workers) + '\n'

        rep += 'WIP: \t {}\n'.format("  ->\t ".join(str(w.wip) for w in self.workers))

        rep += '-------------------------------------\n'
        rep += f'Total Work Done:   {self.work_done}\n'
        rep += f'Total Products Remaining:   {self.total_work}\n'
        rep += f'Workflow WIP: {self.wip}'
        return rep
    
    @classmethod
    def run_chained_process(cls, work=20, workers=4, batch_size=1, verbose=False):
        queue = [Worker(batch_size=batch_size) for _ in range(4)]
        for w1, w2 in zip(queue[:-1], queue[1:]):
            w1.target = w2
        
        workflow = cls(workers=queue)
        steps = workflow.process(work=work, verbose=verbose)
        return steps