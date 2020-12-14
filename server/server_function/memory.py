client_to_user_id = {}
user_id_to_sc = {}
client_dict = {}

# 不一定是登入状态，只是连接
client_list = []

chat_history = []


def remove_c_from_client_list(sc):
    if sc in client_to_user_id:
        uid = client_to_user_id[sc]
        del client_to_user_id[sc]
        if uid in user_id_to_sc:
            del user_id_to_sc[uid]

    if sc in client_list:
        client_list.remove(sc)

    if sc in client_dict:
        del client_dict[sc]