from asgiref.sync import sync_to_async

from admin_panel.telebot.models import Clients


@sync_to_async()
def create_client(telegram_id, username):
    Clients.objects.get_or_create(telegram_id=telegram_id, username=username)


@sync_to_async()
def get_clients():
    return Clients.objects.values_list('telegram_id', flat=True)


@sync_to_async()
def get_clients_count():
    return Clients.objects.count()
