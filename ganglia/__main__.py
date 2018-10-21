import sys
import ganglia


def main(args=None):
    """The main entry point routine."""
    if args is None:
        args = sys.argv[1:]

    ganglia.ganglia_api()

if __name__ == "__main__":
    main()
