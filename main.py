from lcu_driver import Connector

client = Connector()

@client.ready
async def lcu_ready(connection):
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    data = await summoner.json()
    print(f"accountId: {data['accountId']}")
    print(f"displayName: {data['displayName']}")
    print(f"internalName: {data['internalName']}")
    print(data)

@client.ws.register('/lol-matchmaking/v1/ready-check', event_types=('UPDATE',))
async def auto_accept_match(connection, event):
    if event.data['playerResponse'] == 'None':
        await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')
        print('Accepted the ready check.')

@client.close
async def close(connection):
    print('The client have been closed.')
    await client.stop()

client.start()