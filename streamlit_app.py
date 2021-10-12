# -*- coding: utf-8 -*-
"""
@author: HZU
"""
import streamlit as st
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
from utils.plot_functions import plot_image_input_FFT, plot_image_input, plot_predict_histo, plot_same_label_img
from fft_2 import preprocess_input, fft_detector

st.set_page_config(layout="wide")

st.header('THIS IS THE TITLE')
st.subheader(' a lot of text doing all the explanation, because this app has to explain itself ')


st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
##Loading the image to be analize
st.write('here something to load the image.')
image_file = st.file_uploader("Upload File",type=['jpg'])


if image_file is not None:
    file_details = {"FileName":image_file .name,"FileType":image_file.type,"FileSize":image_file.size}
    st.write(file_details)

#Loading the model and also all the classes images to plot
# model = tf.keras.models.load_model('./utils/cnn_model.h5')
img_all_classes = np.load('./utils/img_all_classes.npy')
class_names = [0,1,2,3,4,5,6,7,8,9,10]

with st.expander('CNN method'):
    col_mid, col1, col2, col3, col_end = st.columns(5)
    st.write('here is the method')
    if image_file is not None:
        data = image_file.read()
        dataBytesIO = io.BytesIO(data)
        img = Image.open(dataBytesIO)
        img = np.array(img)
        # prediction = model.predict(img[None,:,:])
        # plot_1 = plot_image_input(img, prediction)
        # plot_2 = plot_predict_histo(prediction)
        # plot_3 = plot_same_label_img(prediction)
        # col1.pyplot(plot_1)
        # col2.pyplot(plot_2)
        # col3.pyplot(plot_3)

with st.expander('FFT method'):
    col_left, col_marg_left, col_center, col_marg_right, col_right = st.columns((1,0.1,1,0.1,1))
    # To play with between 0 (Everything is an anomaly) and 1 (No False Positives on Training)
    predictive_strength = col_center.slider("Precision-Recall Trade-Off", min_value=0.0, max_value=1.0, value=1.0, step=0.05)

    if image_file is not None:
        # data = image_file.read()
        # dataBytesIO = io.BytesIO(data)
        # img = Image.open(dataBytesIO)
        # img = np.array(img)

        processed_image = preprocess_input(img)  # Apply the preprocessing on the matrix image
        detected_anomaly, detected_class, false_positives_on_training_set = fft_detector(processed_image, predictive_strength)

        plot_FFT = plot_image_input_FFT(img, detected_class, detected_anomaly)
        col_left.pyplot(plot_FFT)

        col_center.write("The trade-off between recall and precision generated the following false positives on the Training Set")
        col_center.write(false_positives_on_training_set)
