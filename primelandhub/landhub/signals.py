import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
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

# --- Auto-Train Model on Data Update ---
def train_autoencoder():
    interests = interested.objects.all()
    interest_df = pd.DataFrame(list(interests.values('user_id', 'propertyuser_id', 'interested')))

    if interest_df.empty:
        print("⚠ No user interactions found. Skipping training.")
        return

    # Create user-item matrix
    user_item_matrix = interest_df.pivot_table(index='user_id', columns='propertyuser_id', values='interested', fill_value=0).values
    num_properties = user_item_matrix.shape[1]

    print(f"🔄 Training Autoencoder for {num_properties} properties...")

    # Initialize and train the model
    model = Autoencoder(num_properties).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    for epoch in range(50):
        model.train()
        train_tensor = torch.FloatTensor(user_item_matrix).to(device)
        optimizer.zero_grad()
        output = model(train_tensor)
        loss = criterion(output, train_tensor)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

    # Save trained model
    MODEL_PATH = os.path.join(settings.BASE_DIR, "trained_models", "autoencoder.pth")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)

    print(f"✅ Model updated and saved at {MODEL_PATH}")

# --- Django Signal: Train Model on Data Update ---
@receiver(post_save, sender=property)
@receiver(post_save, sender=interested)
def auto_train_model(sender, instance, **kwargs):
    print("🛠 Detected a new property or user interaction. Updating the model...")
    train_autoencoder()
