from log_monitor import Runner, load_config, default_config
import sys


def main(argv):
    if len(argv) > 1:
        configs = load_config(argv[1])
    else:
        configs = default_config()
    runner = Runner(configs)
    runner.run()


if __name__ == "__main__":
    main(sys.argv)
