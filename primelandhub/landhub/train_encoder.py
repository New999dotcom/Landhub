import os
import sys
import django
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from django.conf import settings

# Django Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "primelandhub.settings")
django.setup()

# Import Django Model
from landhub.models import interested, property

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Define Autoencoder Model ---
class Autoencoder(nn.Module):
    def __init__(self, num_properties):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(num_properties, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, num_properties),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

# --- Load Data ---
interests = interested.objects.filter(interested=True)
properties = property.objects.all()

if not interests.exists() or not properties.exists():
    raise RuntimeError("⚠ No interactions or properties found. Add data first.")

# Convert to DataFrame
interest_df = pd.DataFrame(list(interests.values('user_id', 'propertyuser_id', 'interested')))
prop_df = pd.DataFrame(list(properties.values('id')))

# Ensure property IDs match (fill missing ones)
user_item_matrix = interest_df.pivot_table(index='user_id', columns='propertyuser_id', values='interested', fill_value=0)
user_item_matrix = user_item_matrix.reindex(columns=prop_df['id'], fill_value=0)

# Convert to numpy array
user_item_matrix = user_item_matrix.values
num_properties = user_item_matrix.shape[1]

print(f"Training Autoencoder for {num_properties} properties...")

# Initialize Model
model = Autoencoder(num_properties).to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# Train Model
EPOCHS = 50
for epoch in range(EPOCHS):
    model.train()
    train_tensor = torch.FloatTensor(user_item_matrix).to(device)
    
    optimizer.zero_grad()
    output = model(train_tensor)
    loss = criterion(output, train_tensor)
    loss.backward()
    optimizer.step()
    
    print(f"Epoch {epoch+1}/{EPOCHS}: Loss = {loss.item():.4f}")

# Save Model
MODEL_PATH = os.path.join(settings.BASE_DIR, "trained_models", "autoencoder.pth")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
torch.save(model.state_dict(), MODEL_PATH)

print(f"✅ Model saved at {MODEL_PATH}")
