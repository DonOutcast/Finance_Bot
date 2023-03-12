from controller.controller import Controller
import asyncio

if __name__ == "__main__":
    s = Controller()
    asyncio.run(s.main())
