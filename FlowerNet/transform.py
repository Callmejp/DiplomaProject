# import Image


def number_of_0(x):
    if 1 <= x <= 9:
        return 3
    elif 10 <= x <= 99:
        return 2
    elif 100 <= x <= 999:
        return 1
    else:
        return 0


"""
When you download the dataset you will find that their sizes are irregular,
so l write the code below to transform them to the uniform size(64*64)
"""
# for i in range(1, 1361):
#     length = number_of_0(i)
#     s0 = ""
#     for j in range(length):
#         s0 += "0"
#     image_name = 'image_' + s0 + str(i) + '.jpg'
#     pic_path = '17flowers/jpg/' + image_name
# 
#     pic = Image.open(pic_path, 'r')
#     new_pic = pic.resize((64, 64))
#     new_pic_path = 'flowers/' + image_name
#     new_pic.save(new_pic_path)


