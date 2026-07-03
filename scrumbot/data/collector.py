from langchain_core.documents import Document
from scrumbot.data.chroma import ChromaManager

class DiscordChatCollector:
    """
    DiscordChatCollector to save messages to Chroma.
    """
    def __init__(self):
        self.chroma_manager = ChromaManager()
        self.vectorstore = self.chroma_manager.get_vectorstore()
        
    async def save_message(self, message_id: str, author: str, content: str, timestamp: str, channel: str):
        """
        Saves a discord message to the Chroma vectorstore.
        """
        doc = Document(
            page_content=content,
            metadata={
                "message_id": message_id,
                "author": author,
                "timestamp": timestamp,
                "channel": channel
            }
        )
        # In a real async environment, we might want to use avectorstore methods if available
        # langchain_chroma currently has sync add_documents, we run it in a thread or just call it if it's fast
        self.vectorstore.add_documents([doc])
        
    async def search_messages(self, query: str, k: int = 5) -> list[Document]:
        """
        Searches for related messages.
        """
        return self.vectorstore.similarity_search(query, k=k)
