# Alter-Impl

An alternative implementation that is more congnative friendly. Less things to learn.


### IDEA 1

```python
@task(index=0)
def fn_1():
  ...

@task(index=1)
def fn_2():
  ...

# run all the tasks
run_tasks()
```

### IDEA 2

```python
@task(start=True)
def fn_1():
  ...

@task(depends_on=fn_1)
def fn_2():
  ...

# run all the tasks
run_tasks()
```

### IDEA : Group

@group(id="group2")

```python
@group(id="group1")
@task(start=True)
def fn_1():
  ...

@group(id="group1")
@task()
def fn_2():
  ...

@group(id="group2")
@task()
def fn_3():
  ...

@group(id="group2")
@task()
def fn_4():
  ...

# run all the tasks
run_tasks("group1")
run_tasks(["group1", "group2"])
```

```yml
task:
  start: bool; only one occurrence
  depends_on: function handle
  before: hook before
  after: hook after
  if: precondition to execute this function
group: 
  id: name of a group the task belongs to
```
