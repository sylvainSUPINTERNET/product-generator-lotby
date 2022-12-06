from rembg import remove

input_path = './osef.jpeg'
output_path = './test-output.jpeg'


print("processing ...")

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        t = i.read()
        output = remove(t)
        o.write(output)

