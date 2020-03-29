from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    patient_data = forms.FileField(label="Please upload patient data has a csv file.")

