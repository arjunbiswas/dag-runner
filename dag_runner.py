import logging
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import wait

logging.basicConfig(level=logging.INFO)


def wrap_tasks(*tasks):
    for task in tasks:
        task(1)


def get_indent(times):
    indent_degree = []
    for i in range(times):
        indent_degree.append("\t")
    return "".join(indent_degree)


def f1(indent):
    logging.info(get_indent(indent) + "--> f1()")


def f2(indent):
    logging.info(get_indent(indent) + "--> f2()")


def f3(indent):
    logging.info(get_indent(indent) + "--> f3()")
    time.sleep(5)
    logging.info(get_indent(indent) + "<-- f3()")


def f4(indent):
    logging.info(get_indent(indent) + "--> f4()")
    time.sleep(3)
    logging.info(get_indent(indent) + "<-- f4()")


def f5(indent):
    logging.info(get_indent(indent) + "--> f5()")
    time.sleep(2)
    logging.info(get_indent(indent) + "<-- f5()")


def f6(indent):
    logging.info(get_indent(indent) + "--> f6()")


def f7(indent):
    logging.info(get_indent(indent) + "--> f7()")
    time.sleep(2)
    logging.info(get_indent(indent) + "<-- f7()")


def f8(indent):
    logging.info(get_indent(indent) + "--> f8()")
    time.sleep(2)
    logging.info(get_indent(indent) + "<-- f8()")


def f9(indent):
    logging.info(get_indent(indent) + "--> f9()")
    time.sleep(5)
    logging.info(get_indent(indent) + "<-- f9()")


def f10(indent):
    logging.info(get_indent(indent) + "--> f10()")
    time.sleep(5)
    logging.info(get_indent(indent) + "<-- f10()")


class Job:
    def __init__(self, context):  # Constructor
        self.tasks = []
        self.context = context
        self.is_sequential = True
        self.on_completion = None


class Dag:
    def __init__(self, ):  # Constructor
        self.dag_jobs = []
        self.context = {}

    def pipeline(self, *tasks):  # Constructor
        j = Job(self.context)
        for task in tasks:
            j.tasks.append(task)
        self.dag_jobs.append(j)
        pipeline_result = PipelineResult(self)
        return pipeline_result

    def spawns(self, *tasks):  # Constructor
        j = Job(self.context)
        for task in tasks:
            j.tasks.append(task)
        j.is_sequential = False
        self.dag_jobs.append(j)
        spawns_result = SpawnsResult(self)
        return spawns_result

    def run(self):
        stage = 1
        for j in self.dag_jobs:
            if j.is_sequential:
                self.runsync(j, stage)
            else:
                self.runasync(j, stage)
            stage += 1

    def runsync(self, job, stage):
        for task in job.tasks:
            task(stage)

    def runasync(self, job, stage):
        with ProcessPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(task, stage) for task in job.tasks]
            wait(futures, )


class PipelineDsl:
    def __init__(self, dag):  # Constructor
        self.dag = dag

    def spawns(self, *tasks):
        j = Job(self.dag.context)
        for task in tasks:
            j.tasks.append(task)
        j.is_sequential = False
        self.dag.dag_jobs.append(j)
        spawns_result = SpawnsResult(self.dag)
        return spawns_result


class PipelineResult:
    def __init__(self, dag):  # Constructor
        self.dag = dag

    def then(self):
        pipeline_dsl = PipelineDsl(self.dag)
        return pipeline_dsl

    def on_complete(self):
        pass


class SpawnsDsl:
    def __init__(self, dag):  # Constructor
        self.dag = dag

    def pipeline(self, *tasks):  # Constructor
        j = Job(self.dag.context)
        for task in tasks:
            j.tasks.append(task)
        self.dag.dag_jobs.append(j)
        pipeline_result = PipelineResult(self.dag)
        return pipeline_result


class SpawnsResult:
    def __init__(self, dag):  # Constructor
        self.dag = dag
        pass

    def join(self):
        spawns_dsl = SpawnsDsl(self.dag)
        return spawns_dsl

    def on_complete(self):
        pass


# Driver program to the above graph class
if __name__ == "__main__":
    logging.info("running example 1")
    dag = Dag()
    dag.pipeline(f1, f2).then().spawns(f3, f4, f5).join().pipeline(f6, f7, f8).then().spawns(f9, f10).join()
    dag.run()

    logging.info("running example 2")
    dag = Dag()
    dag.spawns(f1, f2, f3).join().pipeline(f4, f5).then().spawns(f6, f7, f8).join().pipeline(f9, f10).then()
    dag.run()

    logging.info("running example 3")
    dag = Dag()
    dag.pipeline(f1, f2, f3, f4, f5, f6, f7, f8).then().spawns(f9, f10, ).join()
    dag.run()

    logging.info("running example 4")
    dag = Dag()
    dag.spawns(f1, f2, f3, f4, f5, f6, f7, f8).join().pipeline(f9, f10, ).then()
    dag.run()

    logging.info("running example 5")
    dag = Dag()
    dag.spawns(wrap_tasks(f1, f2, f3), wrap_tasks(f4, f5, f6), wrap_tasks(f7, f8)).join().pipeline(f9, f10, ).then()
    dag.run()