import asyncio


async def find_divisibles(inrange, div_by):
    print(f'Finding numbers in range {inrange} divisible by {div_by}')
    located = []
    for i in range(inrange):
        if i % div_by == 0:
            located.append(i)
        if i % 50000 == 0:
            await asyncio.sleep(0.00001)
    print(f'Done with numbers in range {inrange} divisible by {div_by}')
    return located


async def main():
    div1 = loop.create_task(find_divisibles(508000, 34113))
    div2 = loop.create_task(find_divisibles(100052, 3210))
    div3 = loop.create_task(find_divisibles(500, 3))
    await asyncio.wait([div1, div2, div3])
    return div1, div2, div3


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        d1, d2, d3 = loop.run_until_complete(main())
        print(d1.result())
    except Exception as e:
        pass
    finally:
        loop.close()
