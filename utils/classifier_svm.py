from sklearn import svm
import pickle
from injector import Module, Key, Injector, inject, singleton, provider
from utils.hrv import hrv as Hrv
from utils.python_firebase_connection import FirebaseConnection
import asyncio
import numpy as np

class Classifier(object):

    features = 29
    features_index = 9

    def __init__(self):
        self.classifier = svm.SVC()
        self.firebase = FirebaseConnection()
        self.check_existing_file()
    
    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(Classifier, cls).__new__(cls)
       return cls.instance

    def get_classification(self,hrv):
        print("get_classification()")
        return {
                'classificacao' : self.classifier.predict(hrv),
                'musica': hrv
            }

    def _train_classifier(self,array_x,array_y):
        print("train_classifier()")
        self.classifier.fit(array_x,array_y)

    def _check_existing_file(self):
        print("check_existing_file()")
        try:
            with open('svm_training.p','rb') as file:
                self.classifier = pickle.load(file) 
        except Exception as e:
            print("Error while checking file -> {}".format(str(e))) 
            self.prepare_to_fit()
    
    def _dump_training(self):
        print("dump_training()")
        try:
            with open('svm_training.p','wb') as file:
                pickle.dump(self.classifier, file, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
                print("Error while saving training -> {}".format(str(e)))

    def _to_numpy_array(self, dictionary):
        features_values = np.zeros(len(dictionary.keys()),dtype=int)
        for index, (key, value) in enumerate(dictionary.items()):
            features_values[index] = value[0]
        return features_values

    def _prepare_to_fit(self):
        print("prepare_to_fit()")
        data = self.firebase.get_all_data()
        like_dislike_array = np.zeros(len(data), dtype=int)
        hrv = np.empty([len(data),Classifier.features])
        for index, data_value in enumerate(data):
            like_dislike_array[index] = bool(data_value.get('evaluation'))
            hrv[index] = self.to_numpy_array(Hrv(eval(data[0].get('hrv')),16000)[Classifier.features_index])

        self.train_classifier(hrv,like_dislike_array)
        self.dump_training()
    




