from dataclasses import dataclass, field
from typing import Union, Any


@dataclass
class Worker:
    todo: int = 0
    doing: int = 0
    outbox: int = 0
    target: Any = field(default=None, repr=False)
    task_duration: int = field(default=1, repr=False)
    batch_size: int = field(default=1, repr=False)
    max_todo: Union[int, type(None)] = field(default=None, repr=False)
    _task_time: int = field(default=0, repr=False)
    
        
    def work(self):
        
        if not self.doing and self.todo:
            self.todo -= 1
            self.doing += 1
        if self.doing:
            self._task_time += 1
            if self._task_time >= self.task_duration:
                self.doing = 0
                self._task_time = 0
                self.outbox += 1
    
    def push(self):
        if self.outbox >= self.batch_size:
            to_push = self.batch_size
        elif self.outbox and not any([self.todo, self.doing]):
            to_push = self.outbox
        else:
            to_push = 0
        
        if not self.target:
            self.outbox -= to_push
        elif not self.target.max_todo:
            self.target.todo += to_push
            self.outbox -= to_push
        elif self.target.max_todo >= self.target.todo + self.target.doing + to_push:
            self.target.todo += to_push
            self.outbox -= to_push
            if self.batch_size > self.target.max_todo:
                raise ValueError("target's max_todo is smaller than worker's batch size.  No pushing possible.")
                    
        
    @property
    def wip(self):
        return self.todo + self.doing

Worker(todo=3)