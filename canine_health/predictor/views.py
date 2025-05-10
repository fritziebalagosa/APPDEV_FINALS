from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io, base64
from .forms import PredictionForm

# Load model and encoders once
model = joblib.load("predictor/models/canine_model.pkl")
encoders = joblib.load("predictor/models/canine_label_encoders.pkl")
target_encoder = joblib.load("predictor/models/canine_target_encoder.pkl")
feature_order = joblib.load("predictor/models/canine_feature_order.pkl")

def home(request):
    return render(request, 'predictor/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'predictor/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('predict')
    else:
        form = AuthenticationForm()
    return render(request, 'predictor/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def predict_view(request):
    result = None

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            input_data = []

            # Mapping of form fields to trained model feature names
            field_mapping = {
                'age': 'Age',
                'weight': 'Weight (lbs)',
                'spay_neuter_status': 'Spay/Neuter Status',
                'daily_activity_level': 'Daily Activity Level',
                'diet': 'Diet',
                'hours_of_sleep': 'Hours of Sleep',
                'play_time': 'Play Time (hrs)',
                'annual_vet_visits': 'Annual Vet Visits',
                'breed_size': 'Breed Size'
            }

            try:
                # Use only the fields expected by the model
                filtered_features = [f for f in feature_order if f in field_mapping.values()]

                for trained_field in filtered_features:
                    form_field = next((k for k, v in field_mapping.items() if v == trained_field), None)
                    if form_field is None:
                        raise ValueError(f"No matching form field for feature '{trained_field}'.")

                    value = form.cleaned_data.get(form_field)
                    if value is None:
                        raise ValueError(f"Missing value for: {form_field}")

                    print(f"🔍 Processing '{trained_field}' with value '{value}'")

                    # Encode categorical values using encoders
                    if trained_field in encoders:
                        value = encoders[trained_field].transform([str(value)])[0]
                        print(f" Encoded '{trained_field}' -> {value}")
                    else:
                        value = float(value)
                        print(f" Converted '{trained_field}' to float: {value}")

                    input_data.append(value)

                input_df = pd.DataFrame([input_data], columns=filtered_features)
                prediction = model.predict(input_df)[0]

                # Interpret prediction manually (0 or 1)
                if prediction == 1:
                    result = "Your dog is healthy!"
                    
                else:
                            result = "Your dog is not healthy."

            except Exception as e:
                result = f"Prediction error: {e}"

    else:
        form = PredictionForm()

    return render(request, 'predictor/predict.html', {'form': form, 'result': result})


@login_required
def dashboard_view(request):
    df = pd.read_csv("predictor/data/synthetic_dog_breed_health_data.csv")
    fig, ax = plt.subplots()
    df['Healthy'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title("Health Distribution")

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'predictor/dashboard.html', {'chart': image})
