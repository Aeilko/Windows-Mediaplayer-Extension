import asyncio

from winrt.windows.media import MediaPlaybackType
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager, \
	GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus, MediaPropertiesChangedEventArgs, \
	GlobalSystemMediaTransportControlsSession


class WindowsMediaPlayerMediaInfo:
	WINDOWS_MEDIAPLAYER_IDS = ['Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic']

	def __init__(self):
		# Current state
		self.__media_info = {}
		self.__new_state = False

		# WinRT stuff
		asyncio.run(self._get_manager())

	def has_new_state(self):
		return self.__new_state

	def get_now_playing_music(self):
		self.__new_state = False

		if self.__media_info["type"] != MediaPlaybackType.MUSIC:
			return None
		if self.__media_info["status"] not in [PlaybackStatus.PLAYING, PlaybackStatus.PAUSED]:
			return None

		return self.__media_info["media"]

	def add_media_changed_handler(self):
		sessions = self.__manager.get_sessions()
		for session in sessions:
			if session.source_app_user_model_id in self.WINDOWS_MEDIAPLAYER_IDS:
				session.add_media_properties_changed(self.media_changed_handler)

	def media_changed_handler(self, session: GlobalSystemMediaTransportControlsSession, event: MediaPropertiesChangedEventArgs):
		self.__media_info = asyncio.run(self._session_to_media_info(session))
		self.__new_state = True

	async def _session_to_media_info(self, session):
		m = await session.try_get_media_properties_async()
		media = {
			"type": m.playback_type,
			"title": m.title,
			"subtitle": m.subtitle,
			"artist": m.artist,
			"album": m.album_title,
			"album_artist": m.album_artist,
			"current_track": m.track_number,
			"album_tracks": m.album_track_count,
			# "thumbnail": m.thumbnail,             		# Has extra requirements, so only add when actually using it
			"genres": list(m.genres),
		}

		t = session.get_timeline_properties()
		timeline = {
			"start": t.start_time,
			"end": t.end_time,
			"position": t.position,
			"last_updated": t.last_updated_time,
			"seek_start": t.min_seek_time,
			"seek_end": t.max_seek_time,
		}

		playback = session.get_playback_info()
		result = {
			"app_id": session.source_app_user_model_id,
			"type": playback.playback_type,
			"status": playback.playback_status,
			"media": media,
			"timeline": timeline,
		}
		return result

	async def _get_manager(self):
		self.__manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
