import client

if __name__ == "__main__":
    while True:
        # TCP
        try:
            client.tcp_server()
        except :
            pass