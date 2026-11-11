import os
import re
import ctypes
import subprocess
import webbrowser
import platform
from pathlib import Path
from urllib.parse import quote_plus, urlencode

BRAVE_PATH = (
    r"C:\Users\Dell\AppData\Local\BraveSoftware"
    r"\Brave-Browser\Application\brave.exe"
)


def open_in_brave(url):
    """Open a website in Brave, falling back to the default browser."""
    try:
        if os.path.exists(BRAVE_PATH):
            subprocess.Popen([BRAVE_PATH, url])
        else:
            webbrowser.open(url)
    except Exception as e:
        print(f"Brave launch error: {e}")
        webbrowser.open(url)


# =====================================
# 1. APPROVED WEBSITES
# =====================================

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chatgpt.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "github": "https://github.com",

    "flipkart": "https://www.flipkart.com",
    "amazon": "https://www.amazon.in",
    "myntra": "https://www.myntra.com",
    "meesho": "https://www.meesho.com",
    "snapdeal": "https://www.snapdeal.com",
    "snap deal": "https://www.snapdeal.com",
    "ajio": "https://www.ajio.com",
}


# =====================================
# 2. SHOPPING SEARCH
# =====================================

SHOPPING_SEARCH_URLS = {
    "amazon": "https://www.amazon.in/s?k={}",
    "flipkart": "https://www.flipkart.com/search?q={}",
    "myntra": "https://www.myntra.com/{}",
    "meesho": "https://www.meesho.com/search?q={}",
    "snapdeal": "https://www.snapdeal.com/search?keyword={}",
    "ajio": "https://www.ajio.com/search/?text={}",
}


# =====================================
# 3. WINDOWS APPLICATIONS
# =====================================

APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "explorer": ["explorer.exe"],
    "file explorer": ["explorer.exe"],
    "command prompt": ["cmd.exe"],
    "powershell": ["powershell.exe"],

    "vscode": [
        r"C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    ],

    "vs code": [
        r"C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    ],

    "visual studio code": [
        r"C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    ],

    "chrome": ["cmd", "/c", "start", "", "chrome"],
    "edge": ["cmd", "/c", "start", "", "msedge"],

    "whatsapp": [
        "explorer.exe",
        r"shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
    ],

    "whatsapp desktop": [
        "explorer.exe",
        r"shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
    ],

    "chatgpt desktop": [
        "explorer.exe",
        r"shell:AppsFolder\OpenAI.ChatGPT-Desktop_2p2nqsd0c76g0!ChatGPT"
    ],
}


# =====================================
# 4. FOLDERS
# =====================================

FOLDERS = {
    "desktop": Path.home() / "Desktop",
    "documents": Path.home() / "Documents",
    "downloads": Path.home() / "Downloads",
}


# =====================================
# 5. RESPONSE FUNCTION
# =====================================

def response(message):
    return {
        "reply": message,
        "action": "system"
    }


# =====================================
# MEDIA AND VOLUME CONTROL
# =====================================

def press_media_key(key):
    ctypes.windll.user32.keybd_event(
        key, 0, 0, 0
    )

    ctypes.windll.user32.keybd_event(
        key, 0, 2, 0
    )


MEDIA_KEYS = {
    "play_pause": 0xB3,
    "next": 0xB0,
    "previous": 0xB1,
    "volume_up": 0xAF,
    "volume_down": 0xAE,
    "mute": 0xAD,
}


# =====================================
# 6. WHATSAPP MESSAGING
# =====================================

def send_whatsapp_message(phone, message):

    phone = re.sub(r"\D", "", phone)

    if len(phone) < 10 or len(phone) > 15:
        return response("Please provide a valid phone number.")

    if not message.strip():
        return response("Please provide a message.")

    params = urlencode({
        "phone": phone,
        "text": message
    })

    whatsapp_url = f"whatsapp://send?{params}"

    try:

        os.startfile(whatsapp_url)

        return response(
            "WhatsApp is opening with your message. "
            "Please review and click Send."
        )

    except Exception as error:

        return response(
            f"Unable to open WhatsApp: {error}"
        )


# =====================================
# 7. MAIN COMMAND HANDLER
# =====================================

def handle_system_command(message):

    msg = message.lower().strip()

    # Remove Hey Supreme
    msg = re.sub(
        r"^hey supreme[\s,]*",
        "",
        msg
    )

    # Remove ending punctuation
    msg = msg.rstrip(" .!?")

    print("SUPREME RECEIVED:", repr(message))
    print("SUPREME NORMALIZED:", repr(msg))

    
    # =================================
    # MEDIA AND VOLUME COMMANDS
    # =================================
    if msg in ["pause music", "pause song", "stop music"]:
        press_media_key(MEDIA_KEYS["play_pause"])
        return response("Music paused.")

    if msg in ["resume music", "continue music", "play music"]:
        press_media_key(MEDIA_KEYS["play_pause"])
        return response("Resuming music.")

    if msg in ["next song", "next track", "skip song"]:
        press_media_key(MEDIA_KEYS["next"])
        return response("Playing next song.")

    if msg in ["previous song", "previous track", "last song"]:
        press_media_key(MEDIA_KEYS["previous"])
        return response("Playing previous song.")

    if msg in ["volume up", "increase volume"]:
        press_media_key(MEDIA_KEYS["volume_up"])
        return response("Volume increased.")

    if msg in ["volume down", "decrease volume"]:
        press_media_key(MEDIA_KEYS["volume_down"])
        return response("Volume decreased.")

    if msg in ["mute", "mute volume"]:
        press_media_key(MEDIA_KEYS["mute"])
        return response("Volume mute toggled.")

    if msg in ["unmute", "unmute volume"]:
        press_media_key(MEDIA_KEYS["mute"])
        return response("Volume mute toggled.")


    # =================================
    # 8. SHOPPING SEARCH
    # =================================

    shopping_match = re.fullmatch(
        r"(?:search for|search|find|show me)\s+(.+?)\s+on\s+(amazon|flipkart|myntra|meesho|snapdeal|ajio)",
        msg
    )

    if shopping_match:

        product = shopping_match.group(1).strip()
        website = shopping_match.group(2)

        search_url = SHOPPING_SEARCH_URLS[website].format(
            quote_plus(product)
        )

        open_in_brave(search_url)

        return response(
            f"Searching for {product} on {website.title()}."
        )


    # =================================
    # 9. WHATSAPP MESSAGE
    # =================================

    whatsapp_match = re.fullmatch(
        r"send whatsapp message to ([+\d\s()-]+):\s*(.+)",
        msg
    )

    if whatsapp_match:

        phone = whatsapp_match.group(1)
        whatsapp_message = whatsapp_match.group(2)

        return send_whatsapp_message(
            phone,
            whatsapp_message
        )


    # =================================
    # 10. YOUTUBE MUSIC AUTO SEARCH
    # =================================

    music_patterns = [

        r"play (.+?) on youtube(?: music)?",

        r"play music (?:by|from) (.+)",

        r"open and play (.+)",

        r"play (.+)",
    ]

    for pattern in music_patterns:

        match = re.fullmatch(pattern, msg)

        if match:

            song = match.group(1).strip()

            if song:

                try:

                    import yt_dlp

                    options = {
                        "quiet": True,
                        "no_warnings": True,
                        "extract_flat": True,
                        "noplaylist": True,
                    }

                    with yt_dlp.YoutubeDL(options) as ydl:

                        result = ydl.extract_info(
                            "ytsearch1:" + song,
                            download=False
                        )

                    videos = result.get("entries", [])

                    if not videos:

                        return response(
                            "I couldn't find that song on YouTube."
                        )

                    video_id = videos[0].get("id")

                    if not video_id:

                        return response(
                            "I couldn't retrieve the YouTube video."
                        )

                    video_url = (
                        "https://www.youtube.com/watch?v="
                        + video_id
                        + "&autoplay=1"
                    )

                    webbrowser.open(video_url)

                    return response(
                        f"Opening the YouTube video for {song}."
                    )

                except Exception as error:

                    return response(
                        f"Unable to find the song: {error}"
                    )


    # =================================
    # 11. OPEN WEBSITES AND APPS
    # =================================

    open_match = re.fullmatch(
        r"(?:open|launch|start|go to)\s+(.+)",
        msg
    )

    if open_match:

        name = open_match.group(1).strip()

        # Open website
        if name in WEBSITES:

            webbrowser.open(WEBSITES[name])

            return response(
                f"Opening {name}."
            )

        # Open Windows application
        if name in APPS:

            try:

                subprocess.Popen(
                    APPS[name],
                    shell=False
                )

                return response(
                    f"Opening {name}."
                )

            except Exception as error:

                return response(
                    f"Unable to open {name}: {error}"
                )

        # Open folders
        if name in FOLDERS:

            folder = FOLDERS[name]

            if folder.exists():

                os.startfile(str(folder))

                return response(
                    f"Opening {name}."
                )

        return response(
            f"I don't recognize {name}. "
            "Please add it to my approved list."
        )


    # =================================
    # 12. SYSTEM INFORMATION
    # =================================

    if msg in [
        "system info",
        "computer information",
        "show system information"
    ]:

        return response(

            f"Computer: {platform.node()}\n"

            f"Windows: {platform.platform()}\n"

            f"Processor: {platform.processor()}"

        )

    return None
