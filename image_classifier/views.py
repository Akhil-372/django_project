from django.shortcuts import render, redirect
from .models import UploadImage
from django.conf import settings
from django.templatetags.static import static
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Load your image classification model
model = load_model(os.path.join(settings.BASE_DIR, 'image_classifier_model.h5'))

def predict_image(file_path):
    img=image.load_img(file_path,target_size=(150,150))
    img_array=image.img_to_array(img)
    img_array=np.expand_dims(img_array,axis=0)
    img_array/=255.0
    prediction=model.predict(img_array)
    class_index=np.argmax(prediction)
    classes={}
    i=0
    characters=['brook','chopper','franky','jinbe','luffy','nami','robin','sanji','usopp','zoro']
    for pirate in characters:
        classes[i]=pirate
        i=i+1
    predicted_class=classes[class_index]
    return predicted_class

def index(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['file']
        image_instance = UploadImage(image=uploaded_image)
        image_instance.save()
        file_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.image))
        prediction = predict_image(file_path)
        return render(request, 'result.html', {'filename': image_instance.image.name, 'prediction': prediction})
    return redirect('image_classifier:index')
