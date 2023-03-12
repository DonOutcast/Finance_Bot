from controller.controller import Singleton
import asyncio

if __name__ == "__main__":
    s = Singleton()
    asyncio.run(s.main())
