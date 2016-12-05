import praw, re, imguralbum, os, sys, imgurpython
import urllib.request, urllib.parse, urllib.error
from tokens import app_key, app_secret, access_token, refresh_token, imgur_client_secret, imgur_client_key, imgur_access_token, imgur_refresh_token, album_id
from settings import scopes, user_agent, redirect_url

r = praw.Reddit(user_agent=user_agent, client_id=app_key, client_secret=app_secret)
#r.set_oauth_app_info(client_id=app_key,
#                      client_secret=app_secret,
#                     redirect_uri=redirect_url)
#r.refresh_access_information(refresh_token)

#client = imgurpython.ImgurClient(imgur_client_key, imgur_client_secret, imgur_access_token, imgur_refresh_token)

post_limit = 1000
#gen = r.search('site:imgur.com', subreddit='RWBY', sort='new')
gen = r.subreddit('RWBY').search('site:imgur.com', sort='new')
firstsub = 'HopeTheInfiteMonkeyTheorumIsWrong'
if not os.path.exists('C:\\RWBY'):
    os.makedirs('C:\\RWBY')
f = open('C:\\RWBY\\lastsub.txt', 'r+')
lastsub = f.readline();
f.close()
print('Last submission was ID: ', lastsub)

for sub in gen:
    if firstsub is 'HopeTheInfiteMonkeyTheorumIsWrong':
        firstsub = sub.id
        print('First submission was ID: ', firstsub)
    if sub.id not in lastsub:
        sub.url = sub.url.replace('m.', '')
        if '/imgur.com/a' in sub.url:
            print('Album: ',sub.url)
            downloader = imguralbum.ImgurAlbumDownloader(sub.url)
            print('This albums has ', int(downloader.num_images()/2), 'images')
            downloader.save_images()
            #for (counter, image) in enumerate(downloader.imageIDs, start=1):
                #if counter <= len(downloader.imageIDs) / 2:
                    #client.album_add_images(album_id, image[0])
                    #print('Image added to album')
        elif 'imgur.com/gallery/' in sub.url:
            print('Gallery: ', sub.url)
            downloader = imguralbum.ImgurAlbumDownloader(sub.url.replace('gallery', 'a'))
            print('This albums has ', int(downloader.num_images() / 2), 'images')
            downloader.save_images()
            #for (counter, image) in enumerate(downloader.imageIDs, start=1):
                #if counter <= len(downloader.imageIDs) / 2:
                    #client.album_add_images(album_id, image[0])
                    #print('Image added to album')
        elif 'i.imgur.com/' in sub.url:
            print('Direct Image: ',sub.url)
            path = 'C:\\RWBY\\' + sub.url.split('imgur.com/')[1]
            if os.path.isfile(path):
                print("Skipping, already exists.")
            else:
                try:
                    urllib.request.urlretrieve(sub.url, path)
                except:
                    print('Download failed.')
                    os.remove(path)
            #client.album_add_images(album_id, sub.url.split('imgur.com/')[1].split('.')[0])
            #print('Image added to album')
        elif 'imgur.com/' in sub.url:
            print('Image: ', sub.url)
            path = 'C:\\RWBY\\' + sub.url.split('imgur.com/')[1]+'.png'
            if os.path.isfile(path):
                print("Skipping, already exists.")
            else:
                try:
                    urllib.request.urlretrieve('http://i.imgur.com/'+sub.url.split('imgur.com/')[1]+'.png', path)
                except:
                    print('Download failed.')
                    os.remove(path)
            #client.album_add_images(album_id, sub.url.split('imgur.com/')[1])
            #print('Image added to album')
    else:
        print('Found last submission, ending')
        f = open('C:\\RWBY\\lastsub.txt', 'w')
        f.write(firstsub)
        f.close()
        break

print('Reached end of stream')
f = open('C:\\RWBY\\lastsub.txt', 'w')
f.write(firstsub)
f.close()
sys.exit()