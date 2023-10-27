from faker import Faker

fake = Faker()
data=[]

for i in range(10):
    data.append({
        'nombre': fake.name(),
        'apellido': fake.last_name(),
        'email': fake.email(),
        'clave': fake.password(),
        'fecha_nacimiento': fake.date(),
    })


