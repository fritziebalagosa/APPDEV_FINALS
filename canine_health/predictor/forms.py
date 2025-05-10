from django import forms

class PredictionForm(forms.Form):
    age = forms.FloatField(required=True)
    weight = forms.FloatField(required=True, label="Weight (lbs)")
    
    breed_size = forms.ChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')],
        required=True
    )
    
    spay_neuter_status = forms.ChoiceField(
        choices=[('Neutered', 'Neutered'), ('Spayed', 'Spayed')],
        required=True
    )
    
    daily_activity_level = forms.ChoiceField(
        choices=[
            ('None', 'None'),
            ('Low', 'Low'),
            ('Moderate', 'Moderate'),
            ('Active', 'Active'),
            ('Very Active', 'Very Active')
        ],
        required=True
    )
    
    diet = forms.ChoiceField(
        choices=[
            ('Hard food', 'Hard food'),
            ('Wet food', 'Wet food'),
            ('Special diet', 'Special diet'),
            ('Home cooked', 'Home cooked')
        ],
        required=True
    )
    
    hours_of_sleep = forms.FloatField(required=True)
    play_time = forms.FloatField(required=True)
    annual_vet_visits = forms.FloatField(required=True)
