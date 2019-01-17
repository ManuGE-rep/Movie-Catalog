#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbsetup import Base, Users, Categories, Movies

engine = create_engine('sqlite:///movies.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Users
user1 = Users(name='Admin', email='admin@mail.com', password='Admin')
session.add(user1)
session.commit()


# Categories

cat1 = Categories(name='Action', user_id=1)
session.add(cat1)
session.commit()

cat2 = Categories(name='Comedy', user_id=1)
session.add(cat2)
session.commit()

cat3 = Categories(name='Fantasy', user_id=1)
session.add(cat3)
session.commit()

cat4 = Categories(name='Horror', user_id=1)
session.add(cat4)
session.commit()

cat5 = Categories(name='Science-fiction', user_id=1)
session.add(cat5)
session.commit()

cat6 = Categories(name='Thriller', user_id=1)
session.add(cat6)
session.commit()

cat7 = Categories(name='Western', user_id=1)
session.add(cat7)
session.commit()

cat8 = Categories(name='Animation', user_id=1)
session.add(cat8)
session.commit()

# Movies
movie1 = Movies(title='Men in Black',
                year='1997',
                description='Loosely adapted from The Men in Black comic '
                            'book series created by Lowell Cunningham and '
                            'Sandy Carruthers, the film stars Tommy Lee Jones'
                            ' and Will Smith as two agents of a '
                            'secret organization called the Men in Black, '
                            'who supervise extraterrestrial lifeforms who '
                            'live on Earth and hide their '
                            'existence from ordinary ...',
                cover='https://www.joblo.com/assets/'
                      'images/joblo/posters/2018/12/'
                      'men-in-black-international-poster-xl.jpg',
                category='Science-fiction',
                category_id=5,
                user_id=1)

session.add(movie1)
session.commit()

movie2 = Movies(title='Arrival',
                year='2016',
                description='The film follows a linguist enlisted by the U.S.'
                            ' Army to discover how to communicate with aliens'
                            'who have arrived on Earth, before tensions lead '
                            'to war. ',
                category='Science-fiction',
                category_id=5,
                cover='https://m.media-amazon.com/images/M/'
                'MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_.jpg',
                user_id=1)

session.add(movie2)
session.commit()

movie3 = Movies(title='St-Agatha',
                year='2018',
                description='Set in the 1950s in small-town Georgia, '
                            'a pregnant young woman named Agatha seeks '
                            'refuge in a convent. What first starts out '
                            'as the perfect place to have a child turns '
                            'into a dark layer ',
                category='Horror',
                category_id=4,
                cover='http://fr.web.img5.acsta.net/pictures/18/06/04/14/33/'
                      '3796972.jpg',
                user_id=1)

session.add(movie3)
session.commit()

movie4 = Movies(title='Equalizer 2',
                year='2018',
                description='It follows retired United States Marine and '
                            'ex-DIA agent Robert McCall as he sets out on '
                            'a path of revenge after one of his friends is '
                            'killed. ',
                category='Thriller',
                category_id=6,
                cover='https://media.services.cinergy.ch/media/box1600/'
                      '11311e6b02b6739bde7371639bae60b92e42543b.jpg',
                user_id=1)

session.add(movie4)
session.commit()

movie5 = Movies(title='Aquaman',
                year='2018',
                description='In 1985 Maine, lighthouse keeper Thomas '
                            'Curry rescues Atlanna, the princess of the '
                            'underwater nation of Atlantis, during a storm. '
                            'They eventually fall in love and have a son '
                            'named Arthur, who is born with the power to '
                            'communicate with marine lifeforms.',
                category='Fantasy',
                category_id=3,
                cover='https://www.joblo.com/assets/'
                      'images/joblo/posters/2018/11/'
                      'aquamanrisemainposter.jpg',
                user_id=1)

session.add(movie5)
session.commit()

movie6 = Movies(title='Alpha and Omega',
                year='2010',
                description="In Alberta, Canada's Jasper National Park, "
                            "Kate begins Alpha school with her father "
                            "(Winston) and grows up as a fully trained "
                            "Alpha.",
                category='Animation',
                category_id=8,
                cover='https://upload.wikimedia.org/wikipedia/en/thumb/'
                      'e/e7/Alpha_and_Omega_poster.jpg/'
                      '220px-Alpha_and_Omega_poster.jpg',
                user_id=1)

session.add(movie6)
session.commit()

movie7 = Movies(title='Idiocracy',
                year='2006',
                description="In 2005, United States Army librarian, "
                            "Corporal Joe Bauers, is selected for a suspended"
                            " animation experiment on grounds of average "
                            "appearance, intelligence, behavior, etc. Lacking"
                            " a suitable female candidate within the armed "
                            "forces, they hire Rita, a prostitute whose pimp "
                            "'Upgrayedd' has been bribed to allow her to "
                            "take part.",
                category='Comedy',
                category_id=2,
                cover='http://fr.web.img5.acsta.net/c_215_290/medias/nmedia/'
                      '18/36/25/52/18760611.jpg',
                user_id=1)

session.add(movie7)
session.commit()

movie8 = Movies(title='Hostiles',
                year='2017',
                description='American Western film written and directed by '
                            'Scott Cooper, based on a story by Donald '
                            'E. Stewart.',
                category='Western',
                category_id=7,
                cover='https://encrypted-tbn0.gstatic.com/'
                      'images?q=tbn:ANd9GcSHxV-zwjRL2v-'
                      '4flya4DGRr4iLnAhatwcjNwyBMjaa7Gff1JSeyA',
                user_id=1)

session.add(movie8)
session.commit()


print('Database feeded !')
