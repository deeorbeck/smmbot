import aiohttp
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from data import config



def parse_json(data):
    return json.loads(data)


async def parse_json_async(data):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, parse_json, data)
    return result

class Api:

    def __init__(self):
        self.api_url = config.SMM_API_URL
        self.api_key = config.SMM_API_KEY

    async def order(self, data):
        post_data = {'key': self.api_key, 'action': 'add'}
        post_data.update(data)
        return await self._connect(post_data)

    async def status(self, order_id):
        post_data = {
            'key': self.api_key,
            'action': 'status',
            'order': order_id
        }

        return await self._connect(post_data)

    async def multi_status(self, order_ids):
        post_data = {
            'key': self.api_key,
            'action': 'status',
            'orders': ','.join(map(str, order_ids))
        }
        return await self._connect(post_data)

    async def services(self):
        post_data = {
            'key': self.api_key,
            'action': 'services'
        }
        services = {}
        for service in await self._connect(post_data):
            service['rate'] = float(service['rate'])
            service['price'] = float(service['rate']) / 1000
            service['min'] = int(service['min'])
            service['max'] = int(service['max'])
            service['service'] = int(service['service'])
            services[service['service']] = service
        return services
    async def service(self, id):
        services = await self.services()
        return services[id]

    async def refill(self, order_id):
        post_data = {
            'key': self.api_key,
            'action': 'refill',
            'order': order_id
        }
        return await self._connect(post_data)

    async def multi_refill(self, order_ids):
        post_data = {
            'key': self.api_key,
            'action': 'refill',
            'orders': ','.join(map(str, order_ids))
        }
        return await self._connect(post_data)

    async def refill_status(self, refill_id):
        post_data = {
            'key': self.api_key,
            'action': 'refill_status',
            'refill': refill_id
        }
        return await self._connect(post_data)

    async def multi_refill_status(self, refill_ids):
        post_data = {
            'key': self.api_key,
            'action': 'refill_status',
            'refills': ','.join(map(str, refill_ids))
        }
        return await self._connect(post_data)

    async def cancel(self, order_ids):
        post_data = {
            'key': self.api_key,
            'action': 'cancel',
            'orders': ','.join(map(str, order_ids))
        }
        return await self._connect(post_data)

    async def balance(self):
        post_data = {
            'key': self.api_key,
            'action': 'balance'
        }
        return await self._connect(post_data)

    async def _connect(self, post_data):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)',
            # 'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, data=post_data, headers=headers, ssl=False) as response:
                result = None
                if response.status == 200:
                    text = await response.text()
                    result = await parse_json_async(text)
                return result
# Examples

async def main():
    api = Api()

    services = await api.services()  # Return all services
    print(services)

    service = await api.service(2971)
    print(service)

    balance = await api.balance()  # Return user balance
    print(balance)

    status = await api.status(268714)  # Return status, charge, remains, start count, currency
    print(status)


    # # Add order
    # order = await api.order(
    #     {'service': 2971, 'link': 'https://www.instagram.com/id1y0rbek/', 'quantity': 10})  # Default
    # print(order)
    #

    # order = await api.order({'service': 1, 'link': 'http://example.com/test',
    #                          'comments': "good pic\ngreat photo\n:)\n;)"})  # Custom Comments
    # print(order)
    #
    # order = await api.order(
    #     {'service': 1, 'link': 'http://example.com/test', 'quantity': 100, 'usernames': "test, testing",
    #      'hashtags': "#goodphoto"})  # Mentions with Hashtags
    # print(order)
    #
    # order = await api.order(
    #     {'service': 1, 'link': 'http://example.com/test', 'usernames': "test\nexample\nfb"})  # Mentions Custom List
    # print(order)
    #
    # order = await api.order({'service': 1, 'link': 'http://example.com/test', 'quantity': 1000,
    #                          'username': "test"})  # Mentions User Followers
    # print(order)
    #
    # order = await api.order({'service': 1, 'link': 'http://example.com/test', 'quantity': 1000,
    #                          'media': "http://example.com/p/Ds2kfEr24Dr"})  # Mentions Media Likers
    # print(order)
    #
    # order = await api.order({'service': 1, 'link': 'http://example.com/test'})  # Package
    # print(order)
    #
    # order = await api.order(
    #     {'service': 1, 'link': 'http://example.com/test', 'quantity': 100, 'runs': 10, 'interval': 60})  # Drip-feed
    # print(order)
    #
    # # Old posts only
    # order = await api.order({'service': 1, 'username': 'username', 'min': 100, 'max': 110, 'posts': 0, 'delay': 30,
    #                          'expiry': '11/11/2022'})  # Subscriptions
    # print(order)
    #
    # # Unlimited new posts and 5 old posts
    # order = await api.order({'service': 1, 'username': 'username', 'min': 100, 'max': 110, 'old_posts': 5, 'delay': 30,
    #                          'expiry': '11/11/2022'})  # Subscriptions
    # print(order)
    #
    # order = await api.order(
    #     {'service': 1, 'link': 'http://example.com/test', 'quantity': 100, 'username': "test"})  # Comment Likes
    # print(order)
    #
    # order = await api.order(
    #     {'service': 1, 'link': 'http://example.com/test', 'quantity': 100, 'answer_number': '7'})  # Poll
    # print(order)
    #
    # order = await api.order({'service': 1, 'link': 'http://example.com/test', 'quantity': 100,
    #                          'groups': "group1\ngroup2"})  # Invites from Groups
    # print(order)
    #
    # status = await api.status(order['order'])  # Return status, charge, remains, start count, currency
    # print(status)
    #
    # statuses = await api.multi_status([1, 2, 3])  # Return orders status, charge, remains, start count, currency
    # print(statuses)
    #
    # refill = await api.multi_refill([1, 2])
    # print(refill)
    #
    # refill_ids = [r['refill'] for r in refill if 'refill' in r]
    # if refill_ids:
    #     refill_statuses = await api.multi_refill_status(refill_ids)
    #     print(refill_statuses)
    #

if __name__ == '__main__':
    asyncio.run(main())
