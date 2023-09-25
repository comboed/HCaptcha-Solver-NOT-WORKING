from hcaptcha.client import TLSClient
from hcaptcha.payload.payload import Payload
from hcaptcha.solvers.text.text_solver import TextSolver

class HCaptcha(TLSClient, Payload, TextSolver):
    def __init__(self, site_url, site_key, user_agent):
        self.site_url = site_url
        self.site_key = site_key
        self.user_agent = user_agent
        
        # Call the constructors and pass the Hcaptcha "self" instance
        Payload.__init__(self)
        TLSClient.__init__(self)
        TextSolver.__init__(self)

        # Get HCaptcha version
        self.version = self.get_version()

    def get_version(self):
        response = self.session.get("https://hcaptcha.com/1/api.js").text
        
        if ('var Mi="https://newassets.hcaptcha.com/captcha/v1/' not in response):
            print("[-] Unable to grab new HCaptcha version")
            exit(0)
        return response.split('var Mi="https://newassets.hcaptcha.com/captcha/v1/')[1].split('/')[0]
    
    def get_config(self):
        response = self.session.get("https://hcaptcha.com/checksiteconfig?v={}&host={}&sitekey={}&sc=1&swa=1&spst=0".format(self.version, self.site_url, self.site_key))
        
        if ('"pass":true' not in response.text):
            print("[-] Unable to get captcha config")
        return response.json()["c"]
    
    def get_captcha(self, config, rq_data):
        response = self.session.post("https://hcaptcha.com/getcaptcha/" + self.site_key, headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }, data = self.create_inital_payload(config, rq_data))
        
        text, json = response.text, response.json()
        if ("generated_pass_UUID" in text):
            return json["generated_pass_UUID"]
        elif  ("tasklist" not in text):
            print("[-] Unable to get tasklist")
            return None
        return self.refresh_challenge(config, json["key"], json, rq_data)

    def refresh_challenge(self, config, key, previous_captcha, rq_data):
        response = self.session.post("https://hcaptcha.com/getcaptcha/" + self.site_key, headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }, data = self.create_refresh_payload(config, key, previous_captcha, rq_data))

        text, json = response.text, response.json()
        if ("generated_pass_UUID" in text):
            return json["generated_pass_UUID"]
        elif ("tasklist" not in text):
            print("[-] Unable to refresh tasklist")
            return None
        return json
    
    def check_answers(self, config, key, job_mode, answers):
        response = self.session.post("https://hcaptcha.com/checkcaptcha/{}/{}".format(self.site_key, key), headers = {
            "Content-Type": "application/json"
        }, json = self.create_submission_payload(config, job_mode, answers))
        json = response.json()

        if ("generated_pass_UUID" not in response.text):
            return json["c"]
        return json["generated_pass_UUID"]

    def get_tasks(self, captcha, job_mode):
        tasks = {}
        if (job_mode == "text_free_entry"):
            for task in captcha["tasklist"]:
                tasks[task["task_key"]] = task["datapoint_text"]["en"]
        return tasks

    def solve(self, rq_data = None):
        self.update_session_proxy()
        config = self.get_config()
    
        for _ in range(3):
            captcha = self.get_captcha(config, rq_data)
            if (captcha is not None):
                if (type(captcha) == str):
                    return captcha # Instant pass

                job_mode = captcha["request_type"]                
                if (job_mode == "text_free_entry"):
                    response = self.solve_text_questions(config, captcha["key"], job_mode, self.get_tasks(captcha, job_mode))
                    if (type(response) == str):
                        return response
                    config = response

