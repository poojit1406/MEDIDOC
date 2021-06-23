# Medidoc - An Online Disease Detection Platform

This webapp is developed using Flask Web Framework. The models used to predict the diseases are trained on large Datasets. All the links for datasets and the python notebooks used for model creation are mentioned below in this readme. The webapp can predict following Diseases:

- Brain Tumor
- Malaria
- Pneumonia

## Models with their Accuracy of Prediction

| Disease        | Type of Model            | Accuracy |
| -------------- | ------------------------ | -------- |
| Brain Tumor    | Deep Learning Model(CNN) | 94.02%   |
| Malaria        | Deep Learning Model(CNN) | 95.06%   |
| Pneumonia      | Deep Learning Model(CNN) | 91.28%   |

## NOTE

==> Python version 3.8 was used for the whole project.<br>

## Steps to run this application in your system

1. Clone or download the repo.
2. Open command prompt in the downloaded folder.
3. Create a virtual environment

```
mkvirtualenv environment_name
```

4. Install all the dependencies:

```
pip install -r requirements.txt
```

5. Install XAMPP Server on your pc.

```
start Apache and MySql
```

6. Run phpmyadmin on your browser.
7. Create a database with name "users" and then import the users.sql file in it.
8. Create a password for your phpmyadmin.

```
phpmyadmin-->users(database)-->privelleges-->change password
```

9. Copy that password and change it in main.py file at line 23.
10. Run the application

```
python main.py
```

## Dataset Links

All the datasets were used from kaggle.


- [Brain Tumor Dataset](https://github.com/sajal1302/MEDIDOC/tree/master/dataset/brain_tumor_dataset)
- [Malaria Dataset](https://www.kaggle.com/iarunava/cell-images-for-detecting-malaria)
- [Pneumonia Dataset](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia)

## Links for Python Notebooks used for model creation

- [All Diseases] (https://github.com/sajal1302/MEDIDOC/tree/master/codes)

