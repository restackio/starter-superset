import os
from restack_sdk_cloud import RestackCloud

async def main():
    # Initialize the RestackCloud client with the SDK token from environment variables
    restack_cloud_client = RestackCloud(os.getenv('RESTACK_SDK_TOKEN'))

    # Define the backend application configuration
    superset_app = {
        'name': 'superset',
        'dockerFilePath': 'Dockerfile',

        # This deployment supports a pre-configured Superset product with a managed sql database and redis
        'productName': 'superset'
    }
    await restack_cloud_client.stack({
        'name': 'superset stack',
        'previewEnabled': False,
        'applications': [superset_app],
    })

    # Deploy the stack
    await restack_cloud_client.up()

# Run the main function
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
