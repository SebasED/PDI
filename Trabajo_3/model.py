from keras.models import model_from_json
import numpy as np

class SingLenguageDigitsModel(object):

    DIGITS_LIST = ["9", "0",
                     "7", "6",
                     "1", "8",
                     "4", "3",
                     "2", "5"]

    def __init__(self, model_json_file, model_weights_file):
        # load model from JSON file
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)
        #aca sale error no se por que vrg
        #self.loaded_model._make_predict_function()

    def predict_digit(self, img):
        self.preds = self.loaded_model.predict(img)
        return SingLenguageDigitsModel.DIGITS_LIST[np.argmax(self.preds)]