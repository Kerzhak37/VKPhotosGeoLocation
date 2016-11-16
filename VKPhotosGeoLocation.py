import time
import vk

session = vk.Session('6c0a9e6e7f18995dcf29c7c4863b64bb6f2e8c1a0a92d1673b787b5432d4b3526c9cf99df2270d7714b29')

api = vk.API(session)

friends = api.friends.get()

print(len(friends))
print(friends)

friends = api.friends.get()

friends_info = api.users.get(user_ids=friends)

for friend in friends_info:
    print('ID: %s Имя: %s %s' % (friend['uid'], friend['last_name'],friend['first_name']))

geolocation = []

for id in friends:
    print('Получаем данные пользователя: %s' % id)

    albums = api.photos.getAlbums(owner_id=id)
    print('\t...альбомов %s...' % len(albums))

    for album in albums:

        try:

            photos = api.photos.get(owner_id=id, album_id=album['aid'])
            print('\t\t...обрабатываем фотографии альбома...')

            for photo in photos:

                if 'lat' in photo and 'long' in photo:
                    geolocation.append((photo['lat'], photo['long']))
            print('\t\t...найдено %s фото...' % len(photos))
        except:
            pass

        time.sleep(0.5)

    time.sleep(0.5)

js_code = ""

for loc in geolocation:
    js_code += 'new google.maps.Marker({ position: {lat: %s, lng: %s}, map: map });\n' % (loc[0], loc[1])

html = open('map.html').read()

html = html.replace('/* PLACEHOLDER */', js_code)

f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()