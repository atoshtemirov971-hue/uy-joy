import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class FakeListingDetector:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def extract_features(self, listing):
        features = [
            float(listing.price),
            float(listing.area),
            float(listing.rooms),
            len(listing.title),
            len(listing.description),
            listing.images.count(),
            1 if listing.latitude else 0,
            1 if listing.longitude else 0,
            listing.views_count,
            1 if listing.is_negotiable else 0,
        ]
        return np.array(features).reshape(1, -1)

    def train(self, listings):
        X = []
        y = []
        for listing in listings:
            features = self.extract_features(listing)
            X.append(features[0])
            y.append(1 if listing.is_fake else 0)
        if len(X) > 10:
            X = np.array(X)
            y = np.array(y)
            X = self.scaler.fit_transform(X)
            self.model.fit(X, y)
            self.is_trained = True

    def predict(self, listing):
        score = 0.0
        reasons = []

        if listing.price and listing.area:
            price_per_m2 = float(listing.price) / float(listing.area)
            if price_per_m2 < 100:
                score += 0.3
                reasons.append('Narx juda past')

        if len(listing.description) < 50:
            score += 0.2
            reasons.append('Tavsif juda qisqa')

        if listing.images.count() == 0:
            score += 0.3
            reasons.append('Rasm yo\'q')

        if not listing.latitude or not listing.longitude:
            score += 0.1
            reasons.append('Manzil aniq emas')

        if listing.title.isupper():
            score += 0.1
            reasons.append('Sarlavha katta harflarda')

        is_fake = score >= 0.5

        return {
            'is_fake': is_fake,
            'score': round(score, 2),
            'reasons': reasons,
            'message': 'Soxta e\'lon' if is_fake else 'Haqiqiy e\'lon'
        }