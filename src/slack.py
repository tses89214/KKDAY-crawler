import requests
from logger import setup_logger
from config_parser import config

logger = setup_logger()

def send_slack_notification(message):
    webhook_url = config.get('slack', {}).get('webhook_url')
    
    if not webhook_url:
        logger.error("Slack webhook URL not found in configuration")
        return False

    payload = {
        "text": message
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logger.info("Slack notification sent successfully")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Slack notification: {str(e)}")
        return False

def get_slack_message_template(stats):
    return f"""
:robot_face: *KKDAY Crawler Completed* :checkered_flag:

*Summary:*
• Total Cities Crawled: {stats['total_cities']}
• Total Products Scraped: {stats['total_products']}
• Total Runtime: {stats['total_runtime']:.2f} seconds

*Details:*
{stats['city_details']}

*Status:* {'✅ Success' if stats['success'] else '❌ Failed'}

For more information, please check the logs.
"""

if __name__ == "__main__":
    # Example usage
    example_stats = {
        'total_cities': 3,
        'total_products': 150,
        'total_runtime': 120.5,
        'city_details': "• Tokyo: 50 products\n• New York: 60 products\n• Paris: 40 products",
        'success': True
    }
    message = get_slack_message_template(example_stats)
    send_slack_notification(message)
