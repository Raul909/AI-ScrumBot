import asyncio
from typing import Any, Callable, Coroutine

class RequestQueue:
    """
    RequestQueue class using asyncio.Queue and worker tasks.
    """
    def __init__(self, num_workers: int = 3):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.num_workers = num_workers
        self.workers: list[asyncio.Task] = []
        
    async def start(self):
        """Starts the worker tasks."""
        for i in range(self.num_workers):
            task = asyncio.create_task(self._worker(i))
            self.workers.append(task)
            
    async def stop(self):
        """Stops the worker tasks."""
        for _ in range(self.num_workers):
            await self.queue.put(None)
        await asyncio.gather(*self.workers)
        self.workers.clear()
        
    async def _worker(self, worker_id: int):
        while True:
            item = await self.queue.get()
            if item is None:
                self.queue.task_done()
                break
                
            task_func, args, kwargs = item
            try:
                await task_func(*args, **kwargs)
            except Exception as e:
                print(f"Worker {worker_id} failed on task: {e}")
            finally:
                self.queue.task_done()
                
    async def enqueue(self, task_func: Callable[..., Coroutine[Any, Any, Any]], *args: Any, **kwargs: Any):
        """
        Adds a task to the queue.
        """
        await self.queue.put((task_func, args, kwargs))
