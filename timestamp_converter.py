from datetime import datetime
import re

def standardize_timestamp(timestamp_str):
    """
    Convert various timestamp formats to standard format "YYYY-MM-DD HH:MM:SS"
    
    Args:
        timestamp_str (str): Input timestamp string
        
    Returns:
        str: Standardized timestamp in "YYYY-MM-DD HH:MM:SS" format
    """
    if timestamp_str == "Unknown" or not timestamp_str:
        return "Unknown"
    
    try:
        # Handle "DD Month YYYY, HH:MM" format (e.g., "11 May 2025, 19:20")
        if re.match(r'\d{1,2}\s+[A-Za-z]+\s+\d{4},\s+\d{2}:\d{2}', timestamp_str):
            return datetime.strptime(timestamp_str, "%d %B %Y, %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle "Day HH:MM" format (e.g., "Saturday 19:58")
        if re.match(r'[A-Za-z]+\s+\d{2}:\d{2}', timestamp_str):
            # Get current date
            current_date = datetime.now()
            # Parse the time
            time_part = datetime.strptime(timestamp_str.split()[-1], "%H:%M")
            # Combine with current date
            return current_date.replace(
                hour=time_part.hour,
                minute=time_part.minute
            ).strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle "HH:MM" format (e.g., "00:11")
        if re.match(r'\d{2}:\d{2}', timestamp_str):
            current_date = datetime.now()
            time_part = datetime.strptime(timestamp_str, "%H:%M")
            return current_date.replace(
                hour=time_part.hour,
                minute=time_part.minute
            ).strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle "Sidechats" or other special cases
        if timestamp_str in ["Sidechats"]:
            return "Unknown"
            
        return "Unknown"
        
    except Exception as e:
        print(f"Error converting timestamp '{timestamp_str}': {str(e)}")
        return "Unknown"

def process_messages_file(file_path):
    """
    Process messages.json file and update timestamps
    
    Args:
        file_path (str): Path to messages.json file
    """
    import json
    
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        messages = json.load(f)
    
    # Update timestamps
    for message in messages:
        message['timestamp'] = standardize_timestamp(message['timestamp'])
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

# # Example usage:
# if __name__ == "__main__":
#     process_messages_file("post_data/messages.json") 