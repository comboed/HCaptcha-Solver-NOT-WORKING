from hcaptcha import HCaptcha

if __name__ == "__main__":
    site_url = "discord.com"
    site_key = "b2b02ab5-7dae-4d6f-830e-7b55634c888b"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

    captcha = HCaptcha(site_url, site_key, user_agent)
    while 1:
        token = captcha.solve()
        print(token)