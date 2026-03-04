from constants import RequestType, entity_url
from services.api import create_request
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class PmMiddleware(BaseMiddleware):
  def __init__(self):
    super().__init__()

  async def __call__(
    self,
    handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
    event: TelegramObject,
    data: Dict[str, Any]
  ) -> Any:
    # Получение chat_id
    project_manager = create_request(RequestType.GET.name, entity_url["project_manager"] + f'/{str(event.from_user.id)}')
    if project_manager is None:
      return None
    chat_id = None

    if hasattr(event, 'chat') and event.chat:
      # Если chat есть
      chat_id = event.chat.id
    elif hasattr(event, 'message') and event.message and event.message.chat:
      # Если message есть
      chat_id = event.message.chat.id
    if chat_id and project_manager.get("role") == 'PM':
      # Если chat_id есть и пользователь админ
      return await handler(event, data)
    return None