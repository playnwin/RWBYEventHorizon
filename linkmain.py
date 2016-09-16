import praw, re, imguralbum, os, sys
import urllib.request, urllib.parse, urllib.error
from tokens import app_key, app_secret, access_token, refresh_token
from settings import scopes, user_agent, redirect_url

r = praw.Reddit(user_agent=user_agent)

r.set_oauth_app_info(client_id=app_key,
                      client_secret=app_secret,
                     redirect_uri=redirect_url)
r.refresh_access_information(refresh_token)

user_name = 'VelvetBot'
user = r.get_redditor(user_name)

post_limit = 1000
gen = r.search('site:imgur.com', subreddit='RWBY', sort='new')
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
        if 'imgur.com/a' in sub.url:
            print('Album: ',sub.url)
            downloader = imguralbum.ImgurAlbumDownloader(sub.url)
            print('This albums has ', int(downloader.num_images()/2), 'images')
            downloader.save_images()
        elif 'imgur.com/gallery/' in sub.url:
            print('Gallery: ', sub.url)
            downloader = imguralbum.ImgurAlbumDownloader(sub.url.replace('gallery', 'a'))
            print('This albums has ', int(downloader.num_images() / 2), 'images')
            downloader.save_images()
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