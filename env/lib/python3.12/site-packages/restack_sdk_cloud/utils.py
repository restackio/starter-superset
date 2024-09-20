from colorama import Fore, Style
from git import Repo  # Import GitPython's Repo class

from restack_sdk_cloud.sdk_types import DeployedApplication, DeployedStack, Stack
import restack_sdk_cloud.errorCodes as errorCodes
from typing import Optional

def validate_unique_stack_name(stacks: list[Stack], name: str) -> None:
    stack_exists = any(stack.name == name for stack in stacks)
    if stack_exists:
        print(Fore.RED + Style.BRIGHT + 'Error: ' + Style.RESET_ALL + Fore.YELLOW +
              f'Stacks should have unique names on the same deployment plan. Repeated stack name: {name}' + Style.RESET_ALL)
        raise ValueError('Stacks should have unique names on the same deployment plan.')

def validate_unique_application_name(applications: list[dict]) -> None:
    name_set = set()

    for application in applications:
        if application['name'] in name_set:
            raise ValueError(
                f'Applications should have unique names within the same stack. Repeated name: {application["name"]}'
            )
        name_set.add(application['name'])

def pretty_print_deploy_results(stacks: list[DeployedStack]) -> None:
    for stack in stacks:
        stack_name = stack.get('name', 'Unknown')
        print(Style.BRIGHT + f'\n=== Stack: {Fore.BLUE}{stack_name}{Style.RESET_ALL} ===')

        stack_error = stack.get('error', None)
        if stack_error:
            print(Fore.RED + 'Failed to deploy stack: ' + Fore.YELLOW + stack_error + Style.RESET_ALL)
        else:
            print(Fore.GREEN + 'Stack deployment kicked off successfully' + Style.RESET_ALL)

        for app in stack.get('applications', []):
            # backend needs to send application name
            app_name = app.get('name', '')
            print(Style.BRIGHT + f'\n  --- Application: {Fore.BLUE}{app_name}{Style.RESET_ALL} ---')

            app_error = app.get('error', None)
            if app_error:
                print(Fore.RED + '  Failed to deploy application: ' + Fore.YELLOW + app_error + Style.RESET_ALL)
                if app.get('type', None) == errorCodes.GITHUB_APP_INSTALLATION_REQUIRED:
                    connect_url = ensure_http_prefix(app.get('details', [{}])[0].get('connectUrl', ''))
                    print(Fore.YELLOW + '  You can install the app at: ' + Fore.GREEN + connect_url + Style.RESET_ALL)
            else:
                print(Fore.GREEN + '  Application deployment kicked off successfully' + Style.RESET_ALL)

async def get_git_branch() -> str:
    repo = Repo('.')
    branch = repo.active_branch.name
    return branch

async def get_remote_url() -> str:
    repo = Repo('.')
    remote_url = repo.remotes.origin.url.strip()

    # Convert SSH URL to HTTPS URL if necessary
    if remote_url.startswith('git@github.com:'):
        _, path = remote_url.split(':')
        return f'https://github.com/{path.replace(".git", "")}'

    # Remove .git suffix if present
    https_url = remote_url.replace('.git', '')

    # Ensure the URL starts with https://
    if not https_url.startswith('https://'):
        return f'https://github.com/{"/".join(https_url.split("/")[-2:])}'

    return https_url

def ensure_http_prefix(url: str) -> str:
    if url.startswith('http://'):
        return url

    if not url.startswith('https://'):
        return f'https://{url}'
    return url

def has_application_errors(deployed_stacks: list[DeployedStack]) -> bool:
    return any(
        any(app.error for app in getattr(stack, 'applications', []))
        for stack in deployed_stacks
    )

def get_application_with_github_app_error(deployed_stacks: list[DeployedStack]) -> Optional[DeployedApplication]:
    for stack in deployed_stacks:
        applications = stack.get('applications', [])
        for app in applications:
            if app.get('type') == errorCodes.GITHUB_APP_INSTALLATION_REQUIRED:
                return app
    return None
