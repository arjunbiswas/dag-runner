# dag runner

dag_runner has two main concept:

1. **Pipeline** executes the set of functions in sequential order .
2. **Spawns**   executes the set of functions in concurrent fashion and does not have any ordering guarantee.

## Example 1  
runs f1 and f2 sequentially then f3, f4, f5 in parallel then again f6,f7, f8 in sequence and finally f9, f10
in parallel

![example](images/dag_runner.png)

```python
dag = Dag()
dag.pipeline(f1, f2).then().spawns(f3, f4, f5).join().pipeline(f6, f7, f8).then().spawns(f9, f10).join()
dag.run()
```
## Example 2 
runs f1 , f2 and f3 sequentially then f4, f5 in sequence then again f6,f7, f8 in parallel and finally f9,
f10 in parallel

```python
dag = Dag()
dag.spawns(f1, f2, f3).join().pipeline(f4, f5).then().spawns(f6, f7, f8).join().pipeline(f9, f10).then()
dag.run()
```
## Example 3 
runs f1, f2, f3, f4, f5, f6, f7, f8 in sequence and finally f9, f10 in parallel

```python
dag = Dag()
dag.pipeline(f1, f2, f3, f4, f5, f6, f7, f8).then().spawns(f9, f10, ).join()
dag.run()
```

## Example 4 
runs f1, f2, f3, f4, f5, f6, f7, f8 in parallel and finally f9, f10 in sequence

```python
dag = Dag()
dag.spawns(f1, f2, f3, f4, f5, f6, f7, f8).join().pipeline(f9, f10, ).then()
dag.run()
```

## Example 5 
example wraps (f1, f2, f3), (f4, f5, f6), (f7, f8) in sequence and finally f9, f10 in sequence

```python
dag = Dag()
dag.spawns(wrap_tasks(f1, f2, f3), wrap_tasks(f4, f5, f6), wrap_tasks(f7, f8)).join().pipeline(f9, f10, ).then()
dag.run()
```
