eventlet executor
=====

$ ps -efL
UID        PID  PPID   LWP  C NLWP STIME TTY          TIME CMD
root      7967  7251  7967  2    1 01:40 pts/0    00:00:05 python event_blocking.py

$ pstree -p
    |-sshd(1160)---sshd(7171)---bash(7251)---python(7967)


threading executor
=====

$ ps -efL
UID        PID  PPID   LWP  C NLWP STIME TTY          TIME CMD
root      8079  7251  8079  0    4 01:48 pts/0    00:00:00 python thread_blocking.py
root      8079  7251  8087  0    4 01:48 pts/0    00:00:00 python thread_blocking.py
root      8079  7251  8088  0    4 01:48 pts/0    00:00:00 python thread_blocking.py
root      8079  7251  8089  0    4 01:48 pts/0    00:00:00 python thread_blocking.py

$ pstree -p
    |-sshd(1160)---sshd(7171)---bash(7251)---python(8079)-+-{python}(8087)
                                                          |-{python}(8088)
                                                          `-{python}(8089)

