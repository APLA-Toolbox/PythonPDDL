import src.automated_planer as plarser
import argparse


def main():
    args_parser = argparse.ArgumentParser(
        description="Start parsing Domain and Problem files with PDDL.jl using Python"
    )
    args_parser.add_argument
    args_parser.add_argument("domain", type=str, help="PDDL domain file")
    args_parser.add_argument("problem", type=str, help="PDDL problem file")
    args_parser.add_argument("-v", "--verbose", help="Increases the output's verbosity")
    args = args_parser.parse_args()
    apla_tbx = plarser.AutomatedPlaner(args.domain, args.problem)
    path, time = apla_tbx.dijktra_best_first_search(time_it=True)
    print(apla_tbx.get_actions_from_path(path))
    print("Computation time: %.2f" % time)


if __name__ == "__main__":
    main()
