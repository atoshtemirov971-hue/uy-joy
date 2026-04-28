class FakeListingDetector:
    def __init__(self):
        self.is_trained = False

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