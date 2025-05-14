# Facebook Messenger Bot

A Python-based bot for automating Facebook Messenger interactions and message extraction.

## Features

- Automated login to Facebook Messenger
- Cookie-based authentication
- Message extraction from conversations
- Message data saved in JSON format

## Setup

1. Install required packages:
```bash
pip install selenium python-dotenv
```

2. Create a `.env` file with the following variables:
```env
MESSAGE_CONTAINER_XPATH="your_xpath_here"
MESSAGE_XPATH="your_xpath_here"
MESSAGE_XPATH2="your_xpath_here"
SENDER_XPATH="your_xpath_here"
SENDER_XPATH2="your_xpath_here"
MESSAGE_TIME="your_xpath_here"
TOOLTIP_XPATH="your_xpath_here"
```

3. Update the conversation URL in `login.py` with your target conversation.

## Usage

Run the script:
```bash
python main.py
```

## Output

Messages are saved in `post_data/messages.json` with the following structure:
```json
[
    {
        "sender": "Sender Name",
        "text": "Message content",
        "timestamp": "Message timestamp"
    }
]
```

## File Structure

- `login.py`: Main bot implementation
- `main.py`: Script entry point
- `post_data/messages.json`: Extracted message data
- `.env`: Environment variables for XPath selectors
- `messenger_cookies.pkl`: Stored cookies for authentication

## Notes

- The bot uses Selenium WebDriver for automation
- Messages are deduplicated using a combination of sender, text, and timestamp
- The script includes error handling and retry mechanisms
- Cookies are saved to maintain session persistence

## Dependencies

- Python 3.x
- Selenium
- python-dotenv
- Chrome WebDriver 