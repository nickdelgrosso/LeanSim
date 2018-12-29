from leansim import Workflow, Worker
from pytest import fixture
import random

random.seed(10)


@fixture
def wflow():
    workers = [Worker() for _ in range(4)]
    for w1, w2 in zip(workers[:-1], workers[1:]):
        w1.target = w2
    return Workflow(workers=workers)


def test_workflow_measures_wip(wflow):
    assert wflow.wip == 0
    wflow.workers[0].todo = 4
    for el in range(1, 4):
        wflow.step()
        assert wflow.wip == min([el, 4])


def test_process_correct_nsteps_batch(wflow):
    for worker in wflow.workers:
        worker.batch_size = 20
    assert wflow.process(20) == 80


def test_process_correct_nsteps_nobatch(wflow):
    for worker in wflow.workers:
        worker.batch_size = 1
    assert wflow.process(20) == 23


def test_workflow_measures_wip2(wflow):
    for worker in wflow.workers:
        worker.batch_size = 10
    assert wflow.wip == 0
    wflow.workers[0].todo = 10
    for el in range(1, 30):
        wflow.step()
        assert wflow.wip == min([el, 10])


def test_workflow_total_work(wflow):
    wflow.workers[0].todo = 10
    assert wflow.total_work == 10
    assert wflow.wip == 0
    wflow.step()
    assert wflow.total_work == 10
    assert wflow.wip == 1


def test_chain_process_classmethod():
    for _ in range(20):
        workers, work = random.randint(1, 30), random.randint(1, 30)
        assert Workflow.run_chained_process(workers=workers, work=work, batch_size=work) == workers * work
        assert Workflow.run_chained_process(workers=workers, work=work, batch_size=1) == workers + work - 1

