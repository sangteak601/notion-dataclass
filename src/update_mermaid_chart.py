from notion_client import Client


def update_mermaid_pie_chart(
    notion_client : Client,
    page_id : str,
    chart_title : str,
    db_id : str,
    db_filter : dict,
    db_property_category : str,
    db_property_value : str):
    """
    Update a Mermaid chart with data from a Notion database.

    Args:
        notion_client (Client): Notion client object
        page_id (str): Page ID where the chart is located
        chart_title (str): Title of the chart
        db_id (str): Database ID to get data from
        db_filter (dict): Database filter to apply
        db_property_category (str): Database property name to use for categories in the chart. Must be a select property.
        db_property_value (str): Database property name to use for values in the chart. Must be a number property.
    """
    # Get database info
    db_info = notion_client.databases.retrieve(
        **{
            'database_id': db_id,
        }
    )

    # Create dictionary to store chart data
    chart_data = {}
    categories = db_info['properties'][db_property_category]['select']['options']
    for category in categories:
        chart_data[category['name']] = 0

    # Get data from database
    db_data = notion_client.databases.query(
        **{
            'database_id': db_id,
            'filter': db_filter
        }
    )

    # Put data into chart_data
    for result in db_data['results']:
        chart_data[result['properties'][db_property_category]['select']['name']] += result['properties'][db_property_value]['number']

    # Get children of the page
    page_children = notion_client.blocks.children.list(
        **{
            'block_id': page_id,
        }
    )

    # Get the block ID of the chart using the title
    chart_block_id = None
    for result in page_children['results']:
        if result['type'] == 'code':
            if chart_title in result['code']['rich_text'][0]['text']['content']:
                chart_block_id = result['id']
                break

    # Check if chart was found
    if chart_block_id is None:
        raise Exception(f'Chart with title {chart_title} not found on page')

    # Update the chart
    mermaid_script = f'pie showData title {chart_title}\n'
    tab = ' ' * 4
    for category, value in chart_data.items():
        mermaid_script += f'{tab}"{category}": {value}\n'

    # Update the chart block
    notion_client.blocks.update(
        **{
            'block_id': chart_block_id,
            'code': {
                'rich_text': [
                    {
                        'text': {
                            'content': mermaid_script,
                        },
                    },
                ]
            }
        }
    )
