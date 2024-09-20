import colorama
from colorama import Fore, Style
from typing import List
from restack_sdk_cloud.sdk_types import Plan, Stack
import threading

colorama.init(autoreset=True)

def pretty_print_modification_plan(plan: Plan):
    print(f"{Style.BRIGHT}Action: {Fore.GREEN}{plan['action']}")
    print(f"{Style.BRIGHT}Resource Type: {Fore.GREEN}{plan['resourceType']}")
    print(f"{Style.BRIGHT}Changes:")

    for index, change in enumerate(plan['changes']):
        print(f"{Style.BRIGHT}  Change {index + 1}:")
        print(f"    Key: {Fore.CYAN}{change['key']}")
        if change.get('from') is not None:
            print(f"    From: {Fore.RED}{change['from']}")
        if change.get('to') is not None:
            print(f"    To: {Fore.GREEN}{change['to']}")
        if change.get('value') is not None:
            print(f"    Value: {Fore.YELLOW}{change['value']}")

def pretty_print_stack_modification_plan(stacks: List[Stack]):
    print(f"{Style.BRIGHT}\nRestack deployment plan:")

    for index, stack in enumerate(stacks):
        print(f"{Style.BRIGHT}\nStack #{Fore.BLUE}{index + 1}")
        pretty_print_modification_plan(stack['plan'])

        if stack['applications']:
            for ind, application in enumerate(stack['applications']):
                if application['plan']:
                    print(f"{Style.BRIGHT}\nApplication #{Fore.BLUE}{ind + 1}")
                    pretty_print_modification_plan(application['plan'])
                if application.get('databasePlan'):
                    print(f"{Style.BRIGHT}\nDatabase #{Fore.BLUE}{ind + 1}")
                    pretty_print_modification_plan(application['databasePlan'])
        else:
            print(f"{Fore.YELLOW}No applications in this stack.")

def loading_spinner(loading_text: str):
    import itertools
    import sys
    import time
    from colorama import Fore

    spinner = itertools.cycle(['|', '/', '-', '\\'])
    stop_spinner = threading.Event()

    def spinner_task():
        while not stop_spinner.is_set():
            sys.stdout.write(f"\r{Fore.CYAN}{loading_text} {next(spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\n")  # Print a newline after stopping the spinner
        sys.stdout.flush()

    spinner_thread = threading.Thread(target=spinner_task)
    spinner_thread.start()

    return stop_spinner
