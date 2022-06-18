"""
Visualized Traceroute script.
"""
from sys import argv
from scripts.tracert_single import single_lookup


def err():
    print("Invalid argument. Possible arguments: {Domain/IPv4 address}")
    exit()

if __name__ == "__main__":
    """ main function """

    # take user input arguments
    if len(argv) <= 1 or len(argv) > 3:
        err()

    user_in = str(argv[1]).lower()
    single_lookup(user_in)
