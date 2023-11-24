import asyncio
import time

from WindowsMediaPlayerMediaInfo import WindowsMediaPlayerMediaInfo


def media_to_str(media):
    return f"{media['artist']} - {media['title']} ({media['album']})"


def setup(wmediaplayer):
    wmediaplayer.add_media_changed_handler()


async def loop(wmediaplayer):
    print(time.strftime("%H:%M:%S", time.localtime()))
    if wmediaplayer.has_new_state():
        media = wmediaplayer.get_now_playing_music()
        print(f"Now Playing\t\t{media_to_str(media)}")
    await asyncio.sleep(5)


if __name__ == '__main__':
    eloop = asyncio.get_event_loop()
    try:
        wmp = WindowsMediaPlayerMediaInfo()
        setup(wmp)
        while True:
            asyncio.run(loop(wmp))
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down")
        eloop.close()
