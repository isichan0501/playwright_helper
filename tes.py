import difflib

def get_similarity_ratio(str1, str2):
    matcher = difflib.SequenceMatcher(None, str1, str2)
    return matcher.ratio()

def get_next_message(messages, message_templates, similarity_threshold=0.9):
    for template in message_templates:
        found = False
        for message in messages:
            similarity_ratio = get_similarity_ratio(template, message)
            if similarity_ratio >= similarity_threshold:
                found = True
                break
        if not found:
            return template
    return None

message_schema = {
    "type": "sent/received",
    "content": "message content",
    "timestamp": "timestamp value"
}

messages = [
    {"type": "sent", "content": "Hello, nice to meet you!", "timestamp": "2023-06-01 09:00:00"},
    {"type": "received", "content": "I'm good, thank you!", "timestamp": "2023-06-01 09:05:00"},
    {"type": "sent", "content": "Good morning!", "timestamp": "2023-06-01 09:10:00"}
]

message_templates = [
    "Hello, nice to meet you!",
    "Good morning!",
    "How's the weather today?"
]

next_message = get_next_message(messages, message_templates, similarity_threshold=0.9)
print(next_message)
