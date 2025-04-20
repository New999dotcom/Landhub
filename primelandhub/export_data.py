import os
import django
import pandas as pd

# Ensure Django settings are set up correctly
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "primelandhub.settings")  # Update with your actual project name
django.setup()

# Now import the model
from landhub.models import property  # Ensure correct model name from models.py

def export_property_data():
    queryset = property.objects.all()
    data = pd.DataFrame(list(queryset.values()))
    data.to_csv('property_data.csv', index=False)
    print("Exported data successfully to 'property_data.csv'")

if __name__ == "__main__":
    export_property_data()
