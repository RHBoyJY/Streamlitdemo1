# Import necessary libraries 
import numpy as np
import streamlit as st
import utilities  # utilities 模組用於處理資料集和機器學習相關功能的輔助函式。

# Set a title 
st.title("Machine Learning Streamlit App")  # 設置應用程式的標題為"Machine Learning Streamlit App"。

# Add text to the app 
st.write("""
## 探索不同的分類方法		 
在左側更改 分類方法 或 Dataset 以查看不同模型的性能。
""")  # 在應用程式中添加文字，介紹用戶可以探索不同分類方法的功能。

# Add a select box widget to the side 
dataset_name = st.sidebar.selectbox("Select Dataset", ("Iris", "Breast Cancer", "Wine"))  # 在側邊欄添加一個下拉選單，讓用戶選擇資料集。
classifier = st.sidebar.selectbox("Select Classifiers", ("KNN", "SVM", "Random Forest"))  # 在側邊欄添加一個下拉選單，讓用戶選擇分類器。
scaling = st.sidebar.checkbox("Scaling?")  # 在側邊欄添加一個核取方塊，讓用戶選擇是否要對數據進行縮放。
ShowData = st.sidebar.checkbox("Show Data ?")  # 在側邊欄添加一個核取方塊，讓用戶選擇是否要顯示數據。
# Get the data 
X, y = utilities.get_dataset(dataset_name)  # 從 utilities 模組中獲取所選擇的資料集。
col1  , col2 = st.columns([1,3])  # 將應用程式分為兩列。
with col1:  # 在第一列中顯示資料的大小。
	st.write("Shape of the data:", X.shape)  # 在應用程式中顯示資料的大小。
	st.write("Number of Classes:", len(np.unique(y)))  # 在應用程式中顯示類別的種類。

	# Add parameters to the UI based on the classifier
	params = utilities.add_parameter_ui(classifier)  # 根據所選的分類器，在UI上添加相應的參數。
	st.write("**params:** ", params)  # 在應用程式中顯示參數。

	# Get our classifier with the correct classifiers 
	clf = utilities.get_classifier(classifier, params)  # 從 utilities 模組中獲取所選的分類器。

	# Check if scaling is required 
	if scaling:
		X = utilities.scale_data(X)  # 如果用戶選擇了縮放，則對數據進行縮放。

	# Make predictions and get accuray 
	accuracy = utilities.classification(X, y, clf)  # 進行分類並獲取準確度。
	st.write("**Classifer:** ", classifier)  # 在應用程式中顯示所選的分類方法。
	st.write("**Accuracy:** ", accuracy)  # 在應用程式中顯示準確度。

with col2:
	# Plot the components of the data 
	utilities.plot_data(X, y)  # 繪製資料的組件。

if ShowData:
	st.write(X)  # 如果用戶選擇了顯示數據，則在應用程式中顯示數據。
