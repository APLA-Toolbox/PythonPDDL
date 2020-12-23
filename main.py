from jupyddl.automated_planner import AutomatedPlanner
import argparse
import os


def format_output(str):
    copy = str
    # Remove the [ and  ] at both ends
    copy = copy[copy.index("[") + 1 : copy.index("]")]
    ret = ""
    numWords = 0

    # count the number of words
    for i in range(0, len(str)):
        if str[i] == ",":
            numWords = numWords + 1

    # tokenize
    for i in range(1, numWords - 1):
        try:
            new_str = copy[copy.index("<") + 1 : copy.index(">")]
            copy = copy[copy.index(">") + 1 :]
            new_str = new_str[new_str.index(" ") + 1 :]
            ret = ret + new_str + "\n"

        except ValueError as e:
            pass

    print(ret)


def main():
    args_parser = argparse.ArgumentParser(
        description="Start parsing Domain and Problem files with PDDL.jl using Python"
    )
    args_parser.add_argument
    args_parser.add_argument("domain", type=str, help="PDDL domain file")
    args_parser.add_argument("problem", type=str, help="PDDL problem file")
    args_parser.add_argument("-v", "--verbose", help="Increases the output's verbosity")
    args = args_parser.parse_args()
    apla_tbx = AutomatedPlanner(args.domain, args.problem)
    apla_tbx.logger.info("Starting the planning script")
    apla_tbx.logger.debug(
        "Available heuristics: " + str(apla_tbx.available_heuristics.keys())
    )

    path, computation_time = apla_tbx.dijktra_best_first_search(time_it=True)
    apla_tbx.logger.debug(apla_tbx.get_actions_from_path(path))

    apla_tbx.logger.debug("Computation time: %.2f seconds" % computation_time)
    apla_tbx.logger.info("Terminate with grace...")


if __name__ == "__main__":
    main()
