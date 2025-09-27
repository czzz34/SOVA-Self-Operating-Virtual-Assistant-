# functions/chatbot/music_player.py

import yt_dlp
import shutil
import subprocess
import time

try:
    import vlc
except ImportError:
    vlc = None


def play_music(query: str) -> None:
    """
    Search YouTube for `query`, grab the best‐quality audio stream,
    and play it. First tries to launch `cvlc` (console VLC). If `cvlc`
    is not found or fails, falls back to python-vlc.

    This function blocks until playback finishes or errors out.
    If you call it from a GUI, run it inside a separate thread:
        threading.Thread(target=play_music, args=(query,), daemon=True).start()
    """

    def _search_and_get_audio_url(q: str) -> str:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'nocheckcertificate': True,
            'default_search': 'ytsearch',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # "ytsearch1:<q>" → returns one entry (top result)
            info = ydl.extract_info(f"ytsearch1:{q}", download=False)
            entries = info.get('entries', [])
            if not entries:
                raise RuntimeError(f"No YouTube results for: {q!r}")
            video = entries[0]
            title = video.get('title', 'Unknown Title')
            audio_url = video.get('url')
            print(f"▶ Found on YouTube: {title}")
            return audio_url

    def _play_with_cvlc(aurl: str) -> subprocess.Popen:
        cmd = [
            "cvlc",
            "--quiet",
            "--no-video",
            aurl
        ]
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _play_with_python_vlc(aurl: str) -> None:
        if not vlc:
            raise RuntimeError("python-vlc is not installed.")
        instance = vlc.Instance("--no-xlib", "--quiet", "--no-video-title-show")
        player = instance.media_player_new()
        media = instance.media_new(aurl)
        player.set_media(media)
        player.play()
        print("▶ Playing via python-vlc…")
        # Poll until Ended or Error
        while True:
            state = player.get_state()
            if state in (vlc.State.Ended, vlc.State.Error):
                break
            time.sleep(0.5)

    # 1) search YouTube and get direct audio URL
    audio_url = _search_and_get_audio_url(query)

    # 2) try cvlc first (headless VLC). If not found / fails, fallback.
    if shutil.which("cvlc"):
        try:
            proc = _play_with_cvlc(audio_url)
            print("▶ Playing via cvlc (console VLC)…")
            proc.wait()
            return
        except Exception as e:
            print(f"⚠ cvlc playback failed: {e}. Falling back to python-vlc…")
    else:
        print("ℹ `cvlc` not found in PATH. Trying python-vlc…")

    # 3) fallback to python-vlc
    _play_with_python_vlc(audio_url)
