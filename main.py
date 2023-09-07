import sys
import time
from yandex_music import Client
from pypresence import Presence
import os

os.system('pip install yandex-music')
os.system('pip install pypresence')

f = open('yandex_token.txt', 'r')
yan_token = f.read()
f.close()
if yan_token == 'enter your Yandex Music token here':
    print('Please enter your Yandex Music api token into yandex_token.txt')
    time.sleep(5)
    sys.exit()

ym_client = Client(yan_token).init()
discord_rpc = Presence('1149053365158936806')
discord_rpc.connect()
cnt = 0
now_track = ''
secs = 0
mins = 0


def update_discord_rpc():
    zero = ''
    global secs
    global mins
    global cnt
    global now_track
    queues = ym_client.queues_list()
    last_queue = ym_client.queue(queues[0].id)
    last_track_id = last_queue.get_current_track()
    last_track = last_track_id.fetch_track()
    track = last_track.title
    artists = ', '.join(last_track.artists_name())
    cover = last_track.get_cover_url()
    duration = last_track['duration_ms']

    if now_track != track:
        mins = int(duration / 1000) // 60
        secs = int(duration / 1000) - int(duration / 1000) // 60 * 60
        now_track = track
    else:
        if mins == 0 and secs == 0:
            discord_rpc.update(
                details=f'{artists} - {track}',
                state=f'Осталось 0:00',
                large_image=cover,
            )
            return
        if secs == 0:
            secs = 60
            mins -= 1

        secs -= 1
    if len(str(secs)) == 1:
        zero += '0'

    discord_rpc.update(
        details=f'{artists} - {track}',
        state=f'Осталось {mins}:{zero}{secs}',
        large_image=cover,
    )


while True:
    update_discord_rpc()
    time.sleep(1)
