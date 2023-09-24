def get_navigation(user_agent):
    return {
        "vendorSub": "",
        "productSub": "20030107",
        "vendor": "Google Inc.",
        "maxTouchPoints": 0,
        "scheduling": {},
        "userActivation": {},
        "doNotTrack": None,
        "geolocation": {},
        "pdfViewerEnabled": None,
        "webkitTemporaryStorage": {},
        "brave": {},
        "globalPrivacyControl": True,
        "hardwareConcurrency": 12,
        "cookieEnabled": True,
        "appCodeName": "Mozilla",
        "appName": "Netscape",
        "appVersion": user_agent.split("Mozilla/5.0")[0],
        "platform": "Win32",
        "product": "Gecko",
        "userAgent": user_agent,
        "language": "en-US",
        "languages": [
            "en-US",
            "en"
        ],
        "onLine": True,
        "webdriver": False,
        "bluetooth": {},
        "clipboard": {},
        "credentials": {},
        "keyboard": {},
        "managed": {},
        "mediaDevices": {},
        "storage": {},
        "serviceWorker": {},
        "virtualKeyboard": {},
        "wakeLock": {},
        "deviceMemory": 8,
        "ink": {},
        "hid": {},
        "locks": {},
        "gpu": {},
        "mediaCapabilities": {},
        "mediaSession": {},
        "permissions": {},
        "presentation": {},
        "usb": {},
        "xr": {},
        "windowControlsOverlay": {},
        "userAgentData": {
            "brands": [
            {
                "brand": "Brave",
                "version": "117"
            },
            {
                "brand": "Not;A=Brand",
                "version": "8"
            },
            {
                "brand": "Chromium",
                "version": "117"
            }
            ],
            "mobile": False,
            "platform": "Windows"
        },
        "plugins": [
            "internal-pdf-viewer",
            "mhjfbmdgcfjbbpaeojofohoefgiehjai"
        ]
        }

nv = get_navigation("Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41")
print(nv)