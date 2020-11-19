"""
This class serves as the CLI access point to intelligently and selectively access requested data.
The User has the option of receiving ONLY the data they want, or all the data available to them.
Please use this CLI as the starting point for all future expansions.
"""
import asyncio
import sys
import logging
from asynccmd import Cmd                            # pylint: disable=import-error
from data_collection import DataCollection as dc    # pylint: disable=import-error

# Prompts
INTRO = 'Welcome to the Data Management Shell.   Type help or ? to list commands.\n'
PROMPT = '---ENTER COMMAND: '

logging.basicConfig(level=logging.INFO)


class DataShell(Cmd):
    """ Entry Point Command Shell"""
    def __init__(self, mode, intro=INTRO, prompt=PROMPT):
        super().__init__(mode=mode)
        self.data_c = dc()
        self.intro = intro
        self.prompt = prompt
        self.loop = None

    def do_tasks(self, _):
        """ Control Loop"""
        for task in asyncio.Task.all_tasks(loop=self.loop):  # pylint: disable=consider-using-in
            print(task)

    # ----- All actionable commands -----
    def do_req_covid_all(self, _):
        """ Request all covid data"""
        save_frame, do_plot = man_data()
        self.loop.create_task(self.get_covid_data_all(save_frame, do_plot))

    def do_req_cworld(self, _):
        """ Request world covid data"""
        save_frame, do_plot = man_data()
        self.loop.create_task(self.get_covid_data_world(save_frame, do_plot))

    def do_req_ccountry(self, _):
        """ Request covid data by country"""
        countries = []
        while True:
            country = get_input("Next Country: ")
            if country:
                countries.append(country)
            else:
                break
        save_frame, do_plot = man_data()
        self.loop.create_task(self.get_covid_data(countries, save_frame, do_plot))

    def do_terminate(self, _):
        """ Stop the shell and exit:  terminate"""
        logging.info("CLI terminated\n")
        self.loop.stop()
        return True

    def start(self, loop=None):
        """ Start Async Loop"""
        self.loop = loop
        super().cmdloop(loop)

    async def get_covid_data(self, countries, save_frame=False, do_plot=False):
        """ Access point for the async CLI to access country COVID API """
        self.data_c.get_covid_data(countries, save_frame, do_plot)
        return True

    async def get_covid_data_all(self, save_frame=False, do_plot=False):
        """ Access point for the async CLI to access COVID API """
        self.data_c.get_covid_data_all(save_frame, do_plot)
        return True

    async def get_covid_data_world(self, save_frame=False, do_plot=False):
        """ Access point for the async CLI to access World COVID API """
        self.data_c.get_covid_data_world(save_frame, do_plot)
        return True


def man_data():
    """ Additional user spec"""
    save_frame = get_bool("Save Data y/n?")
    do_plot = get_bool("Plot Data y/n?")
    return save_frame, do_plot


def parse(arg):
    """ Parse input"""
    return tuple(map(int, arg.split()))


def get_bool(string):
    """ For string to booleans"""
    value = str(input(string))
    if value == "y" or "yes":
        return True
    return False


def get_input(string):
    """ For string inputs"""
    value = input(string)
    logging.info(value)
    if value in ("end", ""):
        return False
    return value


if sys.platform == 'win32':
    LOOP = asyncio.ProactorEventLoop()
    MODE = "Run"
else:
    LOOP = asyncio.get_event_loop()
    MODE = "Reader"


CMD = DataShell(mode=MODE, intro=INTRO, prompt=PROMPT)
CMD.start(LOOP)

try:
    LOOP.run_forever()
except KeyboardInterrupt:
    LOOP.stop()
