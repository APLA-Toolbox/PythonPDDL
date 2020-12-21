import src.automated_planner as parser
import argparse
import logging
import os


def main():
    args_parser = argparse.ArgumentParser(
        description="Start parsing Domain and Problem files with PDDL.jl using Python"
    )
    args_parser.add_argument
    args_parser.add_argument("domain", type=str, help="PDDL domain file")
    args_parser.add_argument("problem", type=str, help="PDDL problem file")
    args_parser.add_argument("-v", "--verbose", help="Increases the output's verbosity")
    args = args_parser.parse_args()
    logging.basicConfig(
        filename="logs/main.log",
        format="%(levelname)s:%(message)s",
        filemode="w",
        level=logging.INFO,
    )  # Creates the log file
    apla_tbx = parser.AutomatedPlanner(args.domain, args.problem)
    logging.info("Starting the tool")
    path, time = apla_tbx.depth_first_search(time_it=True)
    logging.info(apla_tbx.get_actions_from_path(path))
    logging.info("Computation time: %.2f seconds" % time)
    logging.info("Tool finished")
    # Output the log (to show something in the output screen)
    logfile = open("logs/main.log", "r")
    print(logfile.read())
    logfile.close()


if __name__ == "__main__":
    main()
