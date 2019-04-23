from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
import keras
from keras.models import load_model
import cv2

from form import LoginForm

def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc


app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
count = 0
global graph
graph = tf.get_default_graph()
model = load_model('modules/model2.h5', custom_objects={'auc': auc})  # 选取自己的.h模型名称


@app.route('/', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/uploads',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        result = predict(upload_path)

        return redirect('/res/'+result)

    return render_template('upload.html')


@app.route('/res/<str>', methods=['GET', 'POST'])
def res(str):
    form = LoginForm()
    form.output.data = str
    return render_template('res.html', form=form)


def predict(filename):
    with graph.as_default():
        img = cv2.imread(filename)
        img = cv2.resize(img, (224, 224))
        x = img.copy()
        x.astype(np.float32)
        prediction = model.predict(np.expand_dims(x, axis=0))
        prediction = prediction[0]
        print(prediction)
        if prediction < 0.5:
            res = "猫"
        else:
            res = "狗"

    return res


if __name__ == '__main__':
    app.run(debug=False)
