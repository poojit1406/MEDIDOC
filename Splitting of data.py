import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
from random import shuffle 
import random
import os
from shutil import copyfile
import fastai
from fastai.vision import *

df_train = pd.read_csv('train.csv')
df_test = pd.read_csv('test.csv')

_ = df_train.hist()

x=df_train['id_code']
y=df_train['diagnosis']


print(os.listdir('E:\\4th year project'))


# Creating data into folder format
os.mkdir("E:\\4th year project\\data")
os.mkdir("E:\\4th year project\\data\\train")
for i in range(5):
    os.mkdir("E:\\4th year project\\data\\train\\"+str(i))
def make_img_folder(a, b):
    for id_code ,diagnosis in zip(a,b):
        if diagnosis == 0:
            copyfile('train_images/{}.png'.format(id_code), 'E:\\4th year project\\data\\train\\0\\{}.png'.format(id_code))
        if diagnosis == 1:
            copyfile('train_images/{}.png'.format(id_code), 'E:\\4th year project\\data\\train\\1\\{}.png'.format(id_code))
        if diagnosis == 2:
            copyfile('train_images/{}.png'.format(id_code), 'E:\\4th year project\\data\\train\\2\\{}.png'.format(id_code))
        if diagnosis == 3:
            copyfile('train_images/{}.png'.format(id_code), 'E:\\4th year project\\data\\train\\3\\{}.png'.format(id_code))
        if diagnosis == 4:
            copyfile('train_images/{}.png'.format(id_code), 'E:\\4th year project\\data\\train\\4\\{}.png'.format(id_code))
            
make_img_folder(x, y)

y.value_counts()

