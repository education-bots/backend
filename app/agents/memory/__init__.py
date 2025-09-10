import logging
from typing import Any, Dict, List
from uuid import UUID

from app.db.connection import get_supabase
from app.schemas.agent_schema import Message


logger = logging.getLogger(__name__)


class Memory:
    """Long-term memory using Supabase for conversation persistence"""

    def __init__(self):
        self.supabase = get_supabase()

    
    async def add_message(
        self,
        conversation_id: UUID,
        user_id: UUID,
        message: Message
    ) -> bool:
        """Save conversation to database"""
        
        try:
            # Save conversation metadata
            conversation_data = {
                "user_id": str(user_id),
                "conversation_id": str(conversation_id),
                "role": message["role"],
                "message_text": message["content"],
            }
            
            result = self.supabase.table("messages").insert(conversation_data).execute()
            print(result)
            if result.data:
                logger.info(f"Saved conversation {conversation_id} to database")
                return True
            else:
                logger.error(f"Failed to save conversation {conversation_id}")
                return False
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            return False



    async def get_last_messages(
        self,
        conversation_id: UUID,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get last 5 messages from database"""

        try:            
            result = (
                self.supabase
                    .table("messages")
                    .select('*')
                    .eq("conversation_id", conversation_id)
                    .order("created_at", desc=True)
                    .limit(limit)
                    .execute()
            )

            print(result)
            
            if result.data:
                logger.info(f"Saved conversation {conversation_id} to database")
                return result.data
            else:
                logger.error(f"Failed to save conversation {conversation_id}")
                return []
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            return []


