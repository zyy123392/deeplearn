1.	加载数据集
核心代码如下：
for i in tqdm(range(n//2)):
    X[i] = cv2.resize(cv2.imread('train/cat.%d.jpg' % i), (224, 224))
    X[i+n//2] = cv2.resize(cv2.imread('train/dog.%d.jpg' % i), (224, 224))
2.	分为训练集和验证集
划分训练集使用的是sklearn包下的train_test_split。将训练集和验证集分成了8比2.
3.	构建模型
导出特征向量：利用 model.predict_generator 函数来导出特征向量，最后我们选择了 ResNet50模型
4.	训练模型
model.fit(X_train, y_train, batch_size=16, epochs=3, validation_data=(X_valid, y_valid))

