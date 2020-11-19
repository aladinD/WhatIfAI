""" !@brief Main file to start backend from root of project """

import src.webinterface.backend.api as backend


def main():
    """Main function starting the backend."""
    print("\n---Starting backend---")
    backend.main()


if __name__ == '__main__':
    main()
