from examples.simple import SomeClass
import asyncio


c = SomeClass()


print(asyncio.run(c.bar(1)))
