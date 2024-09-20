import os
import webbrowser
import requests
from colorama import Fore, Style, init

from restack_sdk_cloud.assertions.assertion_stack_plan import assert_is_stack_plan

from restack_sdk_cloud.sdk_types import Stack, StackInput
from restack_sdk_cloud.prompts import loading_spinner, pretty_print_stack_modification_plan
from restack_sdk_cloud.utils import (
    validate_unique_stack_name,
    validate_unique_application_name,
    pretty_print_deploy_results,
    get_git_branch,
    get_remote_url,
    ensure_http_prefix,
    has_application_errors,
    get_application_with_github_app_error,
)
import restack_sdk_cloud.errorCodes as errorCodes

init(autoreset=True)

class RestackCloud:
    def __init__(self, token: str):
        self.token = token
        self.isPlan = os.getenv('RESTACK_CICD') != 'true'
        self.stacks = []
        self.url = 'https://z5d8916c5-z0d84f6e6-gtw.z507f3bcc.blockdev.sh'
        self.stackPlanGenerated = False

    def promptUser(self, question: str) -> bool:
        return input(question).strip().lower() == 'y'

    def deployRestackPlan(self):
        response = requests.post(
            f"{self.url}/sdk/deploy",
            headers={
                'Content-Type': 'application/json',
                'restack-token': self.token,
            },
            json={'stacks': self.stacks}
        )
        return response.json()

    async def stack(self, stackInput: StackInput) -> str:
        validate_unique_stack_name(self.stacks, stackInput['name'])

        if stackInput['applications']:
            validate_unique_application_name(stackInput['applications'])

        try:
            branch = await get_git_branch()
            git_url = await get_remote_url()
        except Exception:
            branch = None
            git_url = None

        print(Fore.GREEN + 'Generating stack plan...')

        payload = {
            'name': stackInput['name'],
            'previewEnabled': stackInput['previewEnabled'],
            'applications': [
                {
                    **app,
                    'gitUrl': app.get('gitUrl', git_url),
                    'gitBranch': app.get('gitBranch', branch),
                    'cloudStorage': app.get('cloudStorage', False),

                    #conditionally add dockerFilePath, dockerBuildContext, image, database if they exist
                    **({'dockerFilePath': app['dockerFilePath'].lstrip('./')} if 'dockerFilePath' in app else {}),
                    **({'dockerBuildContext': app['dockerBuildContext'].lstrip('./')} if 'dockerBuildContext' in app else {}),
                    **({'image': app['image']} if 'image' in app else {}),
                    **({'database': app['database']} if 'database' in app else {})
                } for app in stackInput['applications']
            ]
        }

        response = requests.post(
            f"{self.url}/sdk/plan",
            headers={
                'Content-Type': 'application/json',
                'restack-token': self.token,
            },
            json=payload
        )

        if response.status_code != 200:
            error_message = response.json()
            if error_message.get('error') == errorCodes.INVALID_RESTACK_SDK_TOKEN and error_message.get('createTokenUrl'):
                url = ensure_http_prefix(error_message['createTokenUrl'])
                print(Fore.YELLOW + f"Restack sdk token is invalid.\nPlease create one at {Fore.GREEN + url}")
                webbrowser.open(url)
            else:
                print(Fore.YELLOW + f"Failed to generate stack plan:\n{error_message['error']}")
            return None

        print(Fore.GREEN + 'Stack plan generated successfully')

        data = response.json()

        try:
            assert_is_stack_plan(data)
            self.stacks.append({
                **data['stack'],
                'applications': data['applications']
            })
            self.stackPlanGenerated = True
            return data['stack']['name']
        except Exception as error:
            print(Fore.YELLOW + 'Invalid response from create stack')
            return None

    async def up(self):
        if not self.stackPlanGenerated:
            return

        pretty_print_stack_modification_plan(self.stacks)

        if not self.isPlan:
            print(Fore.GREEN + Style.BRIGHT + 'Deployment confirmed.')
            deploying_interval = loading_spinner('Deploying...')

            data = self.deployRestackPlan()
            # stops spinner
            deploying_interval.set()

            print(Fore.GREEN + Style.BRIGHT + 'Deployment plan kicked off successfully. Follow live status at Restack console: ' + Fore.CYAN + data['stacksUrl'])
            return

        deploy = self.promptUser('Do you wish to deploy these changes? (y/n): ')

        if not deploy:
            print(Fore.YELLOW + 'Deployment cancelled.')
            return

        deploying_interval = loading_spinner('Deploying...')
        data = self.deployRestackPlan()
        # stops spinner
        deploying_interval.set()

        pretty_print_deploy_results(data['stacks'])
        app_with_github_app_error = get_application_with_github_app_error(data['stacks'])

        if app_with_github_app_error and app_with_github_app_error['details'][0].get('connectUrl'):
            webbrowser.open(ensure_http_prefix(app_with_github_app_error['details'][0]['connectUrl']))
            return

        if has_application_errors(data['stacks']):
            return

        print(Fore.GREEN + Style.BRIGHT + f"Follow live status at Restack console: {Fore.CYAN + ensure_http_prefix(data['stacksUrl'])}")
