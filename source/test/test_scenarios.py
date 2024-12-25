from source.configuration.game_config import config


def scenario_1():
    client = config.app.game_client

    client_edit = config.app.client_edit
    client_edit.connect_to_server()
    config.app.map_panel.set_visible()

    # client.is_host = True if client.id == 0 else False
    if client.id == 0:
        client_edit.add_game()
    #     client_edit.join_game(0)
    # else:
    #     client_edit.join_game(0)


#
# import asyncio
#
# async def scenario_1():
#     client = config.app.game_client
#     client_edit = config.app.client_edit
#
#     # Connect to the server
#     await client_edit.connect_to_server()
#
#     # Wait for the ID to be received
#     while client.id is None:
#         await asyncio.sleep(0.1)
#
#     # Wait for 3 seconds
#     await asyncio.sleep(3)
#
#     # Check the ID
#     if client.id == 0:
#         client_edit.add_game()
#         client_edit.join_game(0)
#     else:
#         client_edit.join_game(0)
