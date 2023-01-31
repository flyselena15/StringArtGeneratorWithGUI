from tkinter import *
import tkinter.filedialog
import tkinter as tk
import requests
from tkinter import ttk
import os
from datetime import datetime
from PIL import ImageTk, Image
import matplotlib.pyplot as plt



import csv
import matplotlib.pyplot as plt
from stringart import StringArtGenerator

image_list = {}
def Upload():
    print('upload')
    selectFileName = tk.filedialog.askopenfile(mode='r', title = 'Select a image' )
    filepath = os.path.abspath(selectFileName.name)
    print(filepath)
    path_label.configure(text=filepath)
    
    # Create an object of tkinter ImageTk
    img = Image.open(path_label.cget("text"))
    resize_upload_image = img.resize((200, 200))
    upload_img_tk = ImageTk.PhotoImage(resize_upload_image)
    image_list['upload_img'] = upload_img_tk
    
    # Create a Label Widget to display the text or Image
    imageLabel.configure(image = image_list.get('upload_img'))
    imageLabel.image = image_list.get('upload_img')
    return filepath


def Download():
    link = e1.get()
    files = requests.get(link)
    files.raise_for_status()
    path = tkinter.filedialog.asksaveasfilename()
    print(files.content)
    with open(path, 'wb') as f:
        f.write(files.content)

def Generate():

    # nails_value = int(nails_value)
    # weight_value = int(weight_value)
    # iteration_value = int(iteration_value)

    generator = StringArtGenerator()  
    generator.load_image(path_label.cget("text"))
    generator.preprocess()
    generator.set_nails(int(nails_entry.get())) 
    generator.set_seed(42)
    generator.set_iterations(int(iteration_entry.get()))
    generator.set_shape(combobox_shpae.get())
    generator.set_weight(int(weight_entry.get()))
    pattern = generator.generate()

    # print(img_path_value)
    # print(nails_value)
    # print(iteration_value)
    # print(shape_value)
    # print(weight_value)

    lines_x = []
    lines_y = [] 
    axis_list = []
    for i, j in zip(pattern, pattern[1:]): 
        lines_x.append((i[0], j[0]))
        lines_y.append((i[1], j[1]))
        axis_list.append((i[0], i[1])) 

    axis_w_index = []
    res = []
    point_ref = []
    [res.append(x) for x in axis_list if x not in res]
    axis_w_index.append((0,0.000,0.000,0.000))
    for i in axis_list:
        axis_w_index.append((res.index(i)+1,i[0],i[1],0.000))
    point_ref.append((0,0.000,0.000,0.000))
    for i in res:
        point_ref.append((res.index(i)+1,i[0],i[1],0.000))

    order = []
    for i in axis_w_index:
        order.append((i[0],0.000))

    print(order[0:10])
    print(axis_w_index[0:10])
    
    
    current_dateTime = datetime.now()
    d1 = current_dateTime.strftime("%Y%m%d%H%M%S")


    axis_index_name = os.path.join(os.getcwd(),'StringArt_doc', "axis_w_index_" + d1 + ".txt")
    print(axis_index_name)
    os.makedirs(os.path.dirname(axis_index_name), exist_ok=True)
    f4 = open(axis_index_name, "w+")
    with f4:   
        write = csv.writer(f4)
        write.writerows(axis_w_index)
    f4.close()


    point_ref_name = os.path.join(os.getcwd(), 'StringArt_doc', "point_reference_" + d1 + ".txt")
    os.makedirs(os.path.dirname(point_ref_name), exist_ok=True)
    f = open(point_ref_name, 'w+')
    for t in point_ref:
        line = ' '.join(str(x).strip('(').strip(',').strip(')') for x in t)
        f.write(line + '\n')
    f.close()

    order_name = os.path.join(os.getcwd(), 'StringArt_doc', "order_" + d1 + ".txt")
    os.makedirs(os.path.dirname(order_name), exist_ok=True)
    f5 = open(order_name, 'w+')
    for t in order[1:]:
        line = ' '.join(str(order).strip('(').strip(')') for order in t)
        f5.write(line+'\n')
    f5.close()


    xmin = 0.
    ymin = 0.
    xmax = generator.data.shape[0]
    ymax = generator.data.shape[1]

    plt.ion()
    plt.figure(figsize=(8, 8))
    plt.axis('off')
    axes = plt.gca()
    axes.set_xlim([xmin, xmax])
    axes.set_ylim([ymin, ymax])
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)
    axes.set_aspect('equal')
    plt.draw()

    batchsize = 10
    for i in range(0, len(lines_x), batchsize):
        plt.plot(lines_x[i:i+batchsize], lines_y[i:i+batchsize],
                 linewidth=0.1, color='k')
        plt.draw()
        plt.pause(0.000001)

    save_fig_path = os.path.join(os.getcwd(), 'StringArt_doc', "result_" + d1 + ".png")
    os.makedirs(os.path.dirname(save_fig_path), exist_ok=True)
    plt.savefig(save_fig_path, bbox_inches='tight', pad_inches=0)
    
    result_img = Image.open(save_fig_path)
    resize_result_image = result_img.resize((200, 200))
    result_img_tk = ImageTk.PhotoImage(resize_result_image)
    image_list['result_img'] = result_img_tk

    result_imageLabel.configure(image = image_list.get('result_img'))
    imageLabel.image = image_list.get('result_img')




window = tk.Tk()
window.title('String Art Generator')
window.geometry('600x600')
header_label = tk.Label(window, text='String Art Generator', font = ('Ariel', 20))
header_label.place(relx=0.5, rely=0.05, anchor=CENTER)

return_img_path = tk.StringVar()


# Select canvas shape, rectangle or circle
shape_frame = tk.Frame(window)
# align to shape_frame
option_list = ['rectangle','circle'] # option of canvas
shape_frame.place(relx = 0.05, rely=0.1)
shpae_label = tk.Label(shape_frame, text='Shape of canvas') 
shpae_label.pack(side=tk.LEFT)
combobox_shpae=ttk.Combobox(shape_frame, values=option_list)
combobox_shpae.pack(side=tk.LEFT)
shape_value = combobox_shpae.get()

# Enter nails number
nails_frame = tk.Frame(window)
nails_frame.place(relx = 0.05, rely=0.15)
nails_label = tk.Label(nails_frame, text='Number of nails') 
nails_label.pack(side=tk.LEFT)
nails_entry = tk.Entry(nails_frame)
nails_entry.pack(side=tk.LEFT)
nails_value = nails_entry.get()

# Enter weight 
weight_frame = tk.Frame(window)
weight_frame.place(relx = 0.05, rely=0.2)
weight_label = tk.Label(weight_frame, text='Weight (How dark is your string)') 
weight_label.pack(side=tk.LEFT)
weight_entry = tk.Entry(weight_frame)
weight_entry.pack(side=tk.LEFT)
weight_value = weight_entry.get()


# Enter iteration 
iteration_frame = tk.Frame(window)
iteration_frame.place(relx = 0.05, rely=0.25)
iteration_label = tk.Label(iteration_frame, text='Iteration') 
iteration_label.pack(side=tk.LEFT)
iteration_entry = tk.Entry(iteration_frame)
iteration_entry.pack(side=tk.LEFT)
iteration_value = iteration_entry.get()

# Upload image
image_frame = tk.Frame(window)
image_frame.place(relx = 0.05, rely=0.3)
image_label = tk.Label(image_frame, text='Upload your image') 
image_label.pack(side=tk.LEFT)
img_btn = Button(image_frame, text=' Upload ', command = Upload)
img_btn.pack(side=tk.LEFT)

# img path frame
path_frame = tk.Frame(window)
path_frame.place(relx = 0.05, rely=0.35)
path_label = tk.Label(path_frame, text = '  ')
path_label.pack()
img_path_value = path_label.cget("text")

# Start generating
generate_frame = tk.Frame(window)
generate_frame.place(relx = 0.5, rely= 0.5, anchor=CENTER)
generate_btn = Button(generate_frame, text = ' Generate ', command = Generate)
generate_btn.pack(side=tk.TOP)

# Show Upload image
upload_image_frame = tk.Frame(window)
# upload_image_frame.pack(padx = 10, pady=10, side=tk.LEFT)
upload_image_frame.place(relx = 0.05, rely=0.55)
imageLabel = tk.Label(upload_image_frame)
# imageLabel.grid(row=0,column=1)
imageLabel.pack(side=tk.LEFT)

# Show result image
result_image_frame = tk.Frame(window)
# result_image_frame.pack(padx = 10, pady=10, side=tk.LEFT)
result_image_frame.place(relx = 0.6, rely=0.55)
result_imageLabel = tk.Label(result_image_frame)
result_imageLabel.pack(side = tk.LEFT)
# result_imageLabel.grid(row=0,column=2)





# btn2 = Button(window,text=' Download ', command=Download).grid(row=2, column=0,pady=5)
# btn3 = Button(window,text=' Copy ', ).grid(row=3, column=0,pady=5)

mainloop()
