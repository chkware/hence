# Alternative Implementation

An alternative implementation that is more congnative friendly. Less things to learn.


### IDEA

```python
@task(title="")
def fn_1(**kwargs):
  ...

@task(title="", needs=[fn_1])
def fn_2(**kwargs):
  ...

# run all the tasks
run_tasks([
  fn_1,
  fn_2,
])
```

```python
a_task_group = group("group_for_a_task")

@a_task_group
@task(title="")
def fn_1(**kwargs):
  ...

@a_task_group
@task(title="", needs=[fn_1])
def fn_2(**kwargs):
  ...

run_task_groups([
  a_task_group,
])
```

```python
a_task_group = group("group_for_a_task")

# `needs` means this task depends on given list of groups to executed before
# all the task groups listed to be executed parallely
b_task_group = group("group_for_b_task", needs=[a_task_group, ])


@a_task_group
@task(title="")
def fn_1(**kwargs):
  ...

@a_task_group
@task(title="", needs=[fn_1])
def fn_2(**kwargs):
  ...

run_task_groups([
  b_task_group,
])
```

```python
a_task_group = group("group_for_a_task")

# `needs` means this task depends on given list of groups to executed before
# all the task groups listed to be executed parallely
b_task_group = group("group_for_b_task", needs=[a_task_group, ])


@a_task_group
@task(title="")
def fn_1(**kwargs):
  ...

@a_task_group
@task(title="", needs=[fn_1])
def fn_2(**kwargs):
  ...

# this will run a_task_group twice
run_task_groups([
  a_task_group,
  b_task_group,
])
```

```python
@task(title="")
def fn_1(**kwargs):
  ...

# `needs` means this task depends on given list of task to executed before
# all the task listed to be executed parallely
@task(title="", needs=[fn_1])
def fn_2(**kwargs):
  ...


# `tasks` means list of tasks in the group
# all the task listed to be executed sequencially
a_task_group = group("group_for_a_task", tasks=[fn_1, fn_2])

run_task_groups([
  a_task_group,
])
```
