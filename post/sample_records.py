#post sample records

p1=post(title="Naruto",author=User.objects.get(id=2),genre="action,thriller,comedy",ratings=5.0,content="lorem ipsum")
p2=post(title="Monster",author=User.objects.get(id=3),genre="pycho-thriller,mystery",ratings=4.45,content="lorem ipsum")
p3=post(title="Demon Slayer",author=User.objects.get(id=4),genre="action,slice-of-life,romance",ratings=4.1,content="lorem ipsum")
p4=post(title="Stein Gates",author=User.objects.get(id=5),genre="mystery,thriller",ratings=4.0,content="lorem ipsum")
p5=post(title="Why the hell r u here Sensei?!",author=User.objects.get(id=1),genre="ecchi,romance",ratings=3.98,content="lorem ipsum")