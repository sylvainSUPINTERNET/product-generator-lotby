import base64

with open("./dist/tmp-no-bg.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string)