import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.datasets
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
breast_cancer = sklearn.datasets.load_breast_cancer()
print(breast_cancer)
data_frame = pd.DataFrame(breast_cancer.data,
                          columns=breast_cancer.feature_names)
data_frame['label'] = breast_cancer.target
#print(data_frame.describe())
#print(data_frame['label'].value_counts())

data_frame.groupby('label').mean()
x=data_frame.drop('label',axis=1)
y=data_frame['label']
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=2)
x_train_scaled = StandardScaler().fit_transform(x_train)
x_test_scaled = StandardScaler().fit_transform(x_test)
#print(x_train.shape,x_test.shape,y_train.shape,y_test.shape)
tf.random.set_seed(3)
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(30,)),  
    keras.layers.Dense(20,input_shape=(30,),activation='relu'),
    keras.layers.Dense(2,activation='sigmoid')
])
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
m=model.fit(x_train_scaled,y_train,validation_split=0.1,epochs=10)
model.save('cancer.h5')
input_data=[17.99,10.38,122.8,1001,0.1184,0.2776,0.3001,0.1471,0.2419,0.07871,1.095,0.9053,8.589,153.4,0.006399,0.04904,0.05373,0.01587,0.03003,0.006193,25.38,17.33,184.6,2019,0.1622,0.6656,0.7119,0.2654,0.4601,0.1189]
nparray=np.asarray(input_data)
reshape=nparray.reshape(1,-1)
standarddata=StandardScaler().fit_transform(reshape)
#model.evaluate(x_test_scaled,y_test)
z=model.predict(standarddata)

g=np.argmax(z)
if g==1:
    print("Malignant")
else:
    print("Benign")

