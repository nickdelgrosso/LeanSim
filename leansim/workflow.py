from IPython.display import clear_output
from time import sleep
import os
from .worker import Worker


class Workflow:
    
    def __init__(self, workers):
        self.workers = workers
        
    @property
    def wip(self):
        return sum(w.wip + w.outbox for w in self.workers)
        
    def step(self):
        for worker in self.workers[::-1]:
            worker.push()
            worker.work()

    def process(self, work, verbose=False, sleep_time=0):
        """Returns number of steps to process some piece of work."""
        self.workers[0].todo = 20
        steps = 0
        while self.wip:
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

        rep += 'batch:\t ' + '\t '.join(str(w.batch_size) for w in self.workers) + '\n'
        rep += 'limit:\t ' + '\t '.join(str(w.max_todo) if w.max_todo else "∞" for w in self.workers) + '\n'

        rep += ''.join('\t---' for _ in self.workers) + '\n'

        # for idx, w in enumerate(self.workers):
        #     rep += f'\t-'
        # rep += '\n'
        for attr in ['todo', 'doing', 'outbox']:
                rep += f'{attr}:\t ' + '\t '.join(f'{getattr(w, attr)}' for w in self.workers) + '\n'

        rep += ''.join('\t---' for _ in self.workers) + '\n'

        rep += 'WIP: \t {}\n'.format("  ->\t ".join(str(w.wip) for w in self.workers))

        rep += '-------------------------------------\n'
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