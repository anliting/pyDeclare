import asyncio
class TaskSet:
  def __init__(self):
    self._set=set()
  async def __aenter__(self):
    return self
  async def __aexit__(self,exc_type,exc,tb):
    for t in self._set:
      t.cancel()
    await asyncio.gather(*self._set,return_exceptions=True)
  def create_task(self,coro):
    task=asyncio.create_task(coro)
    self._set.add(task)
    task.add_done_callback(self._set.remove)
    return task
