
class Worker:

    def __init__(self, todo=0, target=None, task_duration=1, batch_size=1, max_todo=None, pull=False, capacity=1):
        self.todo = todo
        self.doing = []
        self.done = 0
        self.target = target
        self.task_duration = task_duration
        self.batch_size = batch_size
        self.max_todo = max_todo
        self.pull = pull
        self.capacity = capacity


    def work(self):
        """Processes work in todo and doing.  Returns amount of work done in this call."""
        
        if len(self.doing) < self.capacity and self.todo:
            for _ in range(min([self.todo, self.capacity])):
                if not self.pull or not self.target or not self.target.max_todo or (self.done + self.target.todo + self.batch_size) <= self.target.max_todo:
                    self.todo -= 1
                    self.doing.append(0)

        work_done = 0
        for idx in reversed(range(len(self.doing))):
            self.doing[idx] += 1
            work_done += 1
            if self.doing[idx] >= self.task_duration:
                self.doing.pop(idx)
                self.done += 1
        return work_done

    
    def push(self):

        if self.target and self.target.max_todo and self.batch_size > self.target.max_todo:
            raise ValueError("target's max_todo is smaller than worker's batch size.  No pushing possible.")

        if self.done >= self.batch_size:
            to_push = self.batch_size
        elif self.done and not any([self.todo, self.doing]):
            to_push = self.done
        else:
            to_push = 0

        if to_push and self.target:
            if not self.target.max_todo or (self.target.max_todo >= self.target.todo + len(self.target.doing) + to_push):
                self.target.todo += to_push
                self.done -= to_push
                    
        
    @property
    def wip(self):
        return self.todo + len(self.doing)

