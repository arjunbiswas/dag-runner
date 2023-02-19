# dag_runner

dag_runner has two main concept:
1. **Pipeline** executes the functions sequentially and in order.
2. **Spawns**   executes the functions concurrently, so there is no ordering guarantee.

## Example 1
![example1](images/1.png)  
```python
dag = Dag()
dag.pipeline(f1, f2).then().spawns(f3, f4, f5).join().pipeline(f6, f7, f8).then().spawns(f9, f10).join()
dag.run()
```
