from rembg import remove

input_path = './osef.jpeg'
output_path = './test-output.jpeg'


print("processing ...")
with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        print("OK")
        t = i.read()
        print(t)
        output = remove(t)
        o.write(output)

