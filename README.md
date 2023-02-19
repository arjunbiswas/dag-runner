# dag_runner

dag_runner has two main concept:
1. **Pipeline** executes the functions sequentially and in order.
2. **Spawns**   executes the functions concurrently, so there is no ordering guarantee.

## Example 1
![example1](images/dag_runner.png)  
```python
dag = Dag()
dag.pipeline(f1, f2).then().spawns(f3, f4, f5).join().pipeline(f6, f7, f8).then().spawns(f9, f10).join()
dag.run()
```

```python
dag = Dag()
dag.spawns(f1, f2, f3).join().pipeline(f4, f5).then().spawns(f6, f7, f8).join().pipeline(f9, f10).then()
dag.run()
```

```python
dag = Dag()
dag.pipeline(f1, f2, f3, f4, f5, f6, f7, f8).then().spawns(f9, f10, ).join()
dag.run()
```

```python
dag = Dag()
dag.spawns(f1, f2, f3, f4, f5, f6, f7, f8).join().pipeline(f9, f10, ).then()
dag.run()
```

```python
dag = Dag()
dag.spawns(wrap_tasks(f1, f2, f3), wrap_tasks(f4, f5, f6), wrap_tasks(f7, f8)).join().pipeline(f9, f10, ).then()
dag.run()
```