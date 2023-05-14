from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .chat import send_receive_chat, get_ext_user, get_messages_history
from .models import ExtUser, Message

# If you don't want to have to login befire accessing the chat, you can remove this decorator
@login_required
def main_view(request):
    # if user is submitting a prompt
    if request.method == 'POST' and 'prompt' in request.POST:
        try:
            prompt = request.POST.get('prompt')
            response = send_receive_chat(prompt, request.user)
            user = get_ext_user(request.user)
            prmpt = Message(role="user", content=prompt, user=user)
            reply = Message(role="assistant", content=response, user=user)
            prmpt.save()
            reply.save()
            return JsonResponse({'response': response})
        except Exception as e:
            print(e)
            return JsonResponse({'error': True, 'msg': str(e)})
        # if user is getting history of messages
    elif request.method == 'POST' and 'history' in request.POST:
        try:
            num = request.POST.get('history')
            response = get_messages_history(request.user, int(num))
            return JsonResponse({'history': response})
        except Exception as e:
            print(e)
            return JsonResponse({'error': True, 'msg': str(e)})
        
    return render(request, 'index.html')
