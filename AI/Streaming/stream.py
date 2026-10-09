

data= ["item1", "item2", "item3"]
def stream_data(data):
    for item in data:
        yield item

for item in stream_data(data):
    print(item)