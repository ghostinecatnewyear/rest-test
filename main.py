import src.args as args
import src.config as config
import src.log as log
import src.request as request


def main():
    config_file = args.parse()
    params = config.parse(config_file)

    try:
        log_file = params['LOG']['FILE']
        api_host = params['API']['HOST']
        api_port = params['API']['PORT']
        login_username = params['LOGIN']['USERNAME']
        login_password = params['LOGIN']['PASSWORD']
        group_name = params['MEDIA_GROUP']['NAME']
        group_description = params['MEDIA_GROUP']['DESCRIPTION']
        player_name = params['MEDIA_PLAYER']['NAME']
        player_description = params['MEDIA_PLAYER']['DESCRIPTION']
        player_mac = params['MEDIA_PLAYER']['MAC']
    except KeyError as e:
        raise Exception(f'undefined config file option {e}')

    log.setup(log_file)

    try:
        client = request.Client(api_host, api_port)
        client.login(login_username, login_password)
        group_id = client.create_group(group_name, group_description)
        player_id = client.create_player(player_name, player_description, player_mac)
        client.add_player_to_group(player_id, group_id)
        client.delete_player(player_id)
        client.delete_group(group_id)
    finally:
        log.shutdown()


main()
