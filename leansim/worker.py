from dataclasses import dataclass, field
from typing import Union, Any


@dataclass
class Worker:
    todo: int = 0
    doing: list = field(default_factory=list, repr=False)
    done: int = 0
    target: Any = field(default=None, repr=False)
    task_duration: int = field(default=1, repr=False)
    batch_size: int = field(default=1, repr=False)
    max_todo: Union[int, type(None)] = field(default=None, repr=False)
    _task_time: int = field(default=0, repr=False)
    pull: bool = field(default=False, repr=False)
    capacity: int = 1


    def work(self):
        """Processes work in todo and doing.  Returns amount of work done in this call."""
        
        if len(self.doing) < self.capacity and self.todo:
            for _ in range(min([self.todo, self.capacity])):
                if not self.pull or not self.target or not self.target.max_todo or (self.done + self.batch_size) < self.target.max_todo:
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

        if to_push:
            if not self.target:
                self.done -= to_push
            elif not self.target.max_todo or (self.target.max_todo >= self.target.todo + len(self.target.doing) + to_push):
                self.target.todo += to_push
                self.done -= to_push
                    
        
    @property
    def wip(self):
        return self.todo + len(self.doing)

