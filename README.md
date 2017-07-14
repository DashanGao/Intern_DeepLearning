# dltool
File List
=============
| File   | Use     |
| -------|:------|
|util.py | general usage |
|plot.py | draw      |
Function
=============
util.py
----------
```Python
def num_extractor(lines, pattern, recall=[-1]):
    :param lines: a string
    :param pattern: pattern to match, put {num} at number you want to extract
                    multi {num} is supported, but not *, / or other special chars
    :param recall: a list marks return index
    :return: a list of extracted number
```
e.g.:   
```Python
pattern = "Iteration {num}, loss = {num}"
recall = [1]
lines = "
I0710 07:38:12.300302 35476 solver.cpp:240] Iteration 398900, loss = 0.0158956\n
I0710 07:38:12.301368 35476 solver.cpp:255]     Train net output #0: loss = 0.00447209 (* 1 = 0.00447209 loss)\n
I0710 07:38:12.301380 35476 solver.cpp:640] Iteration 398900, lr = 0.00442368\n
I0710 07:38:29.711834 35476 solver.cpp:240] Iteration 398950, loss = 0.0173632\n
I0710 07:38:29.711897 35476 solver.cpp:255]     Train net output #0: loss = 0.0222224 (* 1 = 0.0222224 loss)\n
I0710 07:38:29.711911 35476 solver.cpp:640] Iteration 398950, lr = 0.00442368\n
I0710 07:38:53.051653 35476 solver.cpp:344] Model Synchronization Communication time 0.0422409 second\n
I0710 07:38:53.051781 35476 solver.cpp:433] Iteration 399000, Testing net (#0)\n
I0710 07:38:55.725929 35476 solver.cpp:490]     Test net output #0: accuracy_top1 = 0.754062\n
I0710 07:38:55.725968 35476 solver.cpp:490]     Test net output #1: accuracy_top5 = 0.936562\n
I0710 07:38:55.725980 35476 solver.cpp:490]     Test net output #2: loss = 1.51432 (* 1 = 1.51432 loss)\n
I0710 07:38:56.075605 35476 solver.cpp:240] Iteration 399000, loss = 0.0146371\n
I0710 07:38:56.075662 35476 solver.cpp:255]     Train net output #0: loss = 0.00922734 (* 1 = 0.00922734 loss)\n
I0710 07:38:56.075686 35476 solver.cpp:640] Iteration 399000, lr = 0.00442368\n
"

return = np.array([0.0158956, 0.0173632, 0.0146371, 0.00442368])
```
