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

logging.debug("Running Critical Path with H1")
path, metrics = apla.astar_best_first_search(heuristic_key="critical_path/1")
actions = apla.get_actions_from_path(path)
path = Path(path)

logging.debug("Running Critical Path with H2")
path2, metrics2 = apla.astar_best_first_search(heuristic_key="critical_path/2")
actions2 = apla.get_actions_from_path(path2)
path2 = Path(path2)

logging.debug("Running Critical Path with H3")
path3, metrics3 = apla.astar_best_first_search(heuristic_key="critical_path/3")
actions3 = apla.get_actions_from_path(path3)
path3 = Path(path3)

logging.debug("Running Relaxed Critical Path with H1")
path4, metrics4 = apla.astar_best_first_search(heuristic_key="relaxed_critical_path/1")
actions4 = apla.get_actions_from_path(path4)
path4 = Path(path4)

logging.debug("Running Relaxed Critical Path with H2")
path5, metrics5 = apla.astar_best_first_search(heuristic_key="relaxed_critical_path/2")
actions5 = apla.get_actions_from_path(path5)
path5 = Path(path5)

logging.debug("Running Relaxed Critical Path with H3")
path6, metrics6 = apla.astar_best_first_search(heuristic_key="relaxed_critical_path/3")
actions6 = apla.get_actions_from_path(path6)
path6 = Path(path6)

logging.debug("Running Delete Relaxation (HMax)")
path7, metrics7 = apla.astar_best_first_search(heuristic_key="delete_relaxation/h_max")
actions7 = apla.get_actions_from_path(path7)
path7 = Path(path7)

logging.debug("Running Delete Relaxation (HAdd)")
path8, metrics8 = apla.astar_best_first_search(heuristic_key="delete_relaxation/h_add")
actions8 = apla.get_actions_from_path(path8)
path8 = Path(path8)


actions_str = ""
for a in actions:
    actions_str += str(a) + "\n"

actions_str2 = ""
for a in actions2:
    actions_str2 += str(a) + "\n"

actions_str3 = ""
for a in actions3:
    actions_str3 += str(a) + "\n"

actions_str4 = ""
for a in actions4:
    actions_str4 += str(a) + "\n"

actions_str5 = ""
for a in actions5:
    actions_str5 += str(a) + "\n"

actions_str6 = ""
for a in actions6:
    actions_str6 += str(a) + "\n"

actions_str7 = ""
for a in actions7:
    actions_str7 += str(a) + "\n"

actions_str8 = ""
for a in actions8:
    actions_str8 += str(a) + "\n"

dump = (
    "A* - Critical Path - H1\n ======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    "A* - Critical Path - H2\n"
    "======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    "A* - Critical Path - H3\n"
    "======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    "A* - Relaxed Critical Path - H1\n"
    "======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    "A* - Relaxed Critical Path - H2\n"
    "======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    "A* - Relaxed Citical Path - H3\n"
    "======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    "A* - Delete Relaxation - H_Max\n"
    "======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    "A* - Delete Relaxation - H_Add\n"
    "======PLAN (Nodes)=======\n%s\n"
    "======PLAN (Actions)=======\n%s\n"
    "======METRICS=======\n%s\n\n"
    % (
        str(path),
        actions_str,
        str(metrics),
        str(path2),
        actions_str2,
        str(metrics2),
        str(path3),
        actions_str3,
        str(metrics3),
        str(path4),
        actions_str4,
        str(metrics4),
        str(path5),
        actions_str5,
        str(metrics5),
        str(path6),
        actions_str6,
        str(metrics6),
        str(path7),
        actions_str7,
        str(metrics7),
        str(path8),
        actions_str8,
        str(metrics8),
    )
)

f = open(output, "w")
f.write(dump)
f.close()
