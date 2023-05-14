from django.conf import settings
from django.contrib.auth.models import User
import openai
import tiktoken
from .models import ExtUser, Message

# OpenAI API Key
if settings.API_KEY:
    openai.api_key = settings.API_KEY
else:
    raise Exception('OpenAI API Key not found')

# get token and rate limit of the current user
def get_user_limits(username):
    try:
        user = User.objects.get(username=username)
        limits = ExtUser.objects.values('token_limit', 'rate_limit').get(user=user)
        return limits
    except:
        raise("User not found! Ask admin to add your user to chat clients")

# count the tokens in a given string
def count_tokens(prompt):
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

def get_ext_user(username):
    return ExtUser.objects.get(user=User.objects.get(username=username))

# select the max. amount of messages that don't exceed the token limit
def select_messages(username, prompt):
    user = get_ext_user(username)
    limits = get_user_limits(username)
    user_chat_history = Message.objects.filter(user=user).order_by('-id').values('role', 'content')
    systemMsg = {"role": "system", "content":
			"You are a intelligent expert in everything and you're my assistant. write everything in markdown."}
    count = count_tokens(prompt) + count_tokens(systemMsg['content'])
    messages = [
        systemMsg,
    ]
    for msg in user_chat_history:
        if count + count_tokens(msg['content']) < limits['token_limit']:
            messages.insert(
                1, {"role": msg['role'], "content": msg['content']}
            )
            count += count_tokens(msg['content'])
        else:
            break
    
    messages.append({ "role": "user", "content": prompt })

    return messages

# message history for the current user
def get_messages_history(username, num):
    user = get_ext_user(username)
    user_chat_history = Message.objects.filter(user=user).order_by('-id')[:num].values('role', 'content')
    chat_hist = []
    for chat in list(user_chat_history):
        chat_hist.insert(0, chat)
    return chat_hist

# send the prompt and wait for the response
def send_receive_chat(prompt, username):
    messages = select_messages(username, prompt)
    query = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages = messages
    )
    response = query.get('choices')[0]['message']['content']
    return response
