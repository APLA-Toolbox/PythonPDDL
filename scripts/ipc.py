import sys
import logging
import coloredlogs
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from jupyddl.automated_planner import AutomatedPlanner
from jupyddl.node import Path

coloredlogs.install(level="WARNING")

for a in sys.argv:
    if "ipc.py" in a:
        sys.argv.remove(a)
        break

if len(sys.argv) != 3:
    logging.fatal("Binary should be ran with 3 arguments")
    exit()

domain = sys.argv[0]
problem = sys.argv[1]
output = sys.argv[2]

apla = AutomatedPlanner(domain, problem, log_level="WARNING")
path, metrics = apla.astar_best_first_search(heuristic_key="delete_relaxation/h_max")
actions = apla.get_actions_from_path(path)
path = Path(path)
path2, metrics2 = apla.astar_best_first_search(heuristic_key="delete_relaxation/h_add")
actions2 = apla.get_actions_from_path(path2)
path2 = Path(path2)

actions_str = ""
for a in actions:
    actions_str += str(a) + "\n"

actions_str2 = ""
for a in actions2:
    actions_str2 += str(a) + "\n"

dump = (
    "A* - Delete Relaxation - H_Max\n\
        ======PLAN (Nodes)=======\n%s\n\
        ======PLAN (Actions)=======\n%s\n\
        ======METRICS=======\n%s\n\n\
        A* - Delete Relaxation - H_Add\n\
        ======PLAN (Nodes)=======\n%s\n\
        ======PLAN (Actions)=======\n%s\n\
        ======METRICS=======\n%s\n\n"
    % (str(path), actions_str, str(metrics), str(path2), actions_str2, str(metrics2))
)

f = open(output, "w")
f.write(dump)
f.close()
