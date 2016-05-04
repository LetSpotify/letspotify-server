def handle_request(response):
    if response.error:
        print("Error:", response.error)
    else:
        print('called')
        print(response.body)
