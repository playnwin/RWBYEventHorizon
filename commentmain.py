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

user_name = 'VelvetBot'
user = r.redditor(user_name)

post_limit = 1000
gen = user.comments.new(limit=post_limit)
firstcomment = 'HopeTheInfiteMonkeyTheorumIsWrong'
if not os.path.exists('C:\\RWBY'):
    os.makedirs('C:\\RWBY')
f = open('C:\\RWBY\\lastcomment.txt', 'r+')
lastcomment = f.readline();
f.close()
print('Last comment was ID: ', lastcomment)

for com in gen:
    s = re.split("[\\(,\\)]", com.body)
    if firstcomment is 'HopeTheInfiteMonkeyTheorumIsWrong':
        firstcomment = com.id
        print('First comment was ID: ', firstcomment)
    if com.id not in lastcomment:
        for seg in s:
            if '/imgur.com/a' in seg:
                print('Album: ',seg)
                downloader = imguralbum.ImgurAlbumDownloader(seg)
                print('This albums has ', int(downloader.num_images()/2), 'images')
                downloader.save_images()
                #for (counter, image) in enumerate(downloader.imageIDs, start=1):
                    #if counter <= len(downloader.imageIDs) / 2:
                        #client.album_add_images(album_id, image[0])
                        #print('Image added to album')
            elif 'i.imgur.com/' in seg:
                print('Image: ',seg)
                path = 'C:\\RWBY\\' + seg.split('imgur.com/')[1]
                if os.path.isfile(path):
                    print("Skipping, already exists.")
                else:
                    try:
                        urllib.request.urlretrieve(seg, path)
                    except:
                        print('Download failed.')
                        os.remove(path)
                #client.album_add_images(album_id, seg.split('imgur.com/')[1].split('.')[0])
                #print('Image added to album')
    else:
        print('Found last comment, ending')
        f = open('C:\\RWBY\\lastcomment.txt', 'w')
        f.write(firstcomment)
        f.close()
        break

print('Reached end of stream')
f = open('C:\\RWBY\\lastcomment.txt', 'w')
f.write(firstcomment)
f.close()
sys.exit()