from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input

# Define the class labels for the model
class_labels = {
    0: '1',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6'
}


def getPrediction(filename):
    # Load the model
    model = load_model('checkpoint_VGG16_sgd.h5')

    # Load and preprocess the image
    image = load_img('static/uploads/' + filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)

    # Predict the class
    yhat = model.predict(image)

    # Get the class with the highest probability
    class_index = yhat.argmax()
    label = class_labels[class_index]
    probability = yhat[0][class_index] * 100  # Convert to percentage

    # Print the result
    print(f'{label} ({probability:.2f}%)')

    # Return the label and probability
    return label, probability
