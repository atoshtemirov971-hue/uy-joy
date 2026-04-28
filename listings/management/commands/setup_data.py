from django.core.management.base import BaseCommand
from listings.models import Region, District, Category


class Command(BaseCommand):
    help = 'Setup initial data'

    def handle(self, *args, **kwargs):
        # Kategoriyalar
        categories = [
            {'name': 'Kvartira', 'slug': 'kvartira', 'icon': 'fa-building'},
            {'name': 'Uy', 'slug': 'uy', 'icon': 'fa-home'},
            {'name': 'Tijorat', 'slug': 'tijorat', 'icon': 'fa-store'},
            {'name': 'Yer', 'slug': 'yer', 'icon': 'fa-map'},
            {'name': 'Yangi bino', 'slug': 'yangi-bino', 'icon': 'fa-city'},
        ]
        for cat in categories:
            Category.objects.get_or_create(slug=cat['slug'], defaults=cat)
        self.stdout.write('✅ Kategoriyalar qoshildi!')

        # Viloyatlar va tumanlar
        data = {
            'Toshkent shahri': {
                'slug': 'toshkent-shahri',
                'districts': [
                    'Bektemir', 'Chilonzor', 'Hamza', 'Mirobod',
                    'Mirzo Ulugbek', 'Olmazor', 'Sergeli', 'Shayxontohur',
                    'Uchtepa', 'Yakkasaroy', 'Yashnobod', 'Yunusobod',
                ]
            },
            'Toshkent viloyati': {
                'slug': 'toshkent-viloyati',
                'districts': [
                    'Angren', 'Bekobod', 'Bostonliq', 'Buka', 'Chinoz',
                    'Chirchiq', 'Qibray', 'Ohangaron', 'Olmaliq', 'Oqqorgon',
                    'Parkent', 'Piskent', 'Quyi Chirchiq', 'Toshkent tumani',
                    'Yangiyo\'l', 'Yuqori Chirchiq', 'Zangiota',
                ]
            },
            'Samarqand viloyati': {
                'slug': 'samarqand',
                'districts': [
                    'Samarqand shahri', 'Bulung\'ur', 'Ishtixon', 'Jomboy',
                    'Kattaqo\'rg\'on', 'Narpay', 'Nurobod', 'Oqdaryo',
                    'Pastdarg\'om', 'Paxtachi', 'Payariq', 'Qo\'shrabot',
                    'Toyloq', 'Urgut',
                ]
            },
            'Buxoro viloyati': {
                'slug': 'buxoro',
                'districts': [
                    'Buxoro shahri', 'Vobkent', 'G\'ijduvon', 'Jondor',
                    'Kogon', 'Qorovulbozor', 'Olot', 'Peshku', 'Romitan',
                    'Shofirkon', 'Qorako\'l',
                ]
            },
            'Andijon viloyati': {
                'slug': 'andijon',
                'districts': [
                    'Andijon shahri', 'Asaka', 'Baliqchi', 'Bo\'z',
                    'Buloqboshi', 'Izboskan', 'Jalolquduq', 'Xo\'jaobod',
                    'Xonobod', 'Marhamat', 'Oltinko\'l', 'Paxtaobod',
                    'Qo\'rg\'ontepa', 'Shahrixon', 'Ulug\'nor',
                ]
            },
            'Namangan viloyati': {
                'slug': 'namangan',
                'districts': [
                    'Namangan shahri', 'Chortoq', 'Chust', 'Kosonsoy',
                    'Mingbuloq', 'Norin', 'Pop', 'To\'raqo\'rg\'on',
                    'Uchqo\'rg\'on', 'Uychi', 'Yangiqo\'rg\'on',
                ]
            },
            "Farg'ona viloyati": {
                'slug': 'fargona',
                'districts': [
                    "Farg'ona shahri", 'Beshariq', 'Bog\'dod', 'Buvayda',
                    'Dang\'ara', 'Furqat', 'Qo\'qon', 'Qo\'shtepa',
                    'Marg\'ilon', 'Oltiariq', 'Rishton', 'So\'x',
                    'Toshloq', 'O\'zbekiston', 'Yozyovon',
                ]
            },
            'Qashqadaryo viloyati': {
                'slug': 'qashqadaryo',
                'districts': [
                    'Qarshi shahri', 'Chiroqchi', 'Dehqonobod', 'G\'uzor',
                    'Kamashi', 'Kasbi', 'Kitob', 'Koson', 'Mirishkor',
                    'Muborak', 'Nishon', 'Qamashi', 'Shahrisabz', 'Yakkabog\'',
                ]
            },
            'Surxondaryo viloyati': {
                'slug': 'surxondaryo',
                'districts': [
                    'Termiz shahri', 'Angor', 'Bandixon', 'Denov',
                    'Jarqo\'rg\'on', 'Muzrabot', 'Oltinsoy', 'Qiziriq',
                    'Qumqo\'rg\'on', 'Sariosiyo', 'Sherobod', 'Shurchi', 'Uzun',
                ]
            },
            'Xorazm viloyati': {
                'slug': 'xorazm',
                'districts': [
                    'Urganch shahri', 'Bog\'ot', 'Gurlan', 'Xiva',
                    'Xonqa', 'Hazorasp', 'Qo\'shko\'pir', 'Shovot',
                    'Tuproqqal\'a', 'Yangiariq', 'Yangibozor',
                ]
            },
            'Navoiy viloyati': {
                'slug': 'navoiy',
                'districts': [
                    'Navoiy shahri', 'Karmana', 'Konimex', 'Navbahor',
                    'Nurota', 'Qiziltepa', 'Tomdi', 'Uchquduq', 'Xatirchi',
                ]
            },
            'Jizzax viloyati': {
                'slug': 'jizzax',
                'districts': [
                    'Jizzax shahri', 'Arnasoy', 'Baxmal', 'Do\'stlik',
                    'Forish', 'G\'allaorol', 'Mirzacho\'l', 'Paxtakor',
                    'Yangiobod', 'Zarbdor', 'Zafarobod', 'Zomin',
                ]
            },
            'Sirdaryo viloyati': {
                'slug': 'sirdaryo',
                'districts': [
                    'Guliston shahri', 'Boyovut', 'Xavast', 'Mirzaobod',
                    'Oqoltin', 'Sardoba', 'Sayxunobod', 'Shirin',
                    'Sirdaryo tumani',
                ]
            },
            "Qoraqalpog'iston Respublikasi": {
                'slug': 'qoraqalpogiston',
                'districts': [
                    'Nukus shahri', 'Amudaryo', 'Beruniy', 'Chimboy',
                    'Ellikkala', 'Kegeyli', 'Mo\'ynoq', 'Nukus tumani',
                    'Qanliko\'l', 'Qo\'ng\'irot', 'Qorao\'zak',
                    'Shumanay', 'Taxtako\'pir', 'To\'rtko\'l', 'Xo\'jayli',
                ]
            },
        }

        for region_name, region_data in data.items():
            region, _ = Region.objects.get_or_create(
                slug=region_data['slug'],
                defaults={'name': region_name, 'slug': region_data['slug']}
            )
            for district_name in region_data['districts']:
                slug = district_name.lower().replace(' ', '-').replace("'", '').replace('\u2019', '').replace("'", '')
                District.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'name': district_name,
                        'slug': slug,
                        'region': region
                    }
                )
            self.stdout.write(f'✅ {region_name} va tumanlari qoshildi!')

        # Superuser yaratish
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@uyjoy.uz',
                password='Admin12345!'
            )
            self.stdout.write('✅ Superuser yaratildi!')
        else:
            self.stdout.write('✅ Superuser allaqachon bor!')

        self.stdout.write('🎉 Barcha malumotlar muvaffaqiyatli qoshildi!')