import threading
import requests
import time

class TextSolver:
    def __init__(self):
        self.previous_answers = self.load_previous_answers()

    def load_previous_answers(self):
        answers = {}
        with open("./hcaptcha/solvers/text/answers.txt", "r") as file:
            for line in file.read().splitlines():
                answer = line.split(":")
                answers[answer[0]] = answer[1]
            return answers

    def write_answers(self, questions: dict):
        with open("./hcaptcha/solvers/text/answers.txt", "a+") as file:
            previous_questions = self.previous_answers.keys()
            for question, answer in questions.items():
                if (question not in previous_questions):
                    file.write(question + ":" + answer + "\n")

    def create_answer_file(self):
        with open("./hcaptcha/solvers/text/answers.txt", "w") as file:
            for question, answer in self.previous_answers.items():
                file.write(question + ":" + answer + "\n")

    def is_answered(self, tasks: dict, questions):
        for task_key, task_question in tasks.items():
            for answer_question, answer in self.previous_answers.items():
                if (task_question == answer_question):
                    tasks[task_key] = {"text": answer}
                    questions[answer_question] = answer
        return all(value == "text" for value in tasks.keys())
    
    def remove_answers(self, questions: dict):
        previous_questions = self.previous_answers.keys()
        for question in questions.keys():
            if question in previous_questions:
                self.previous_answers.pop(question)
        self.create_answer_file()

    def ask_question(self, tasks, questions, task_key, question):
        for _ in range(3):
            response = requests.post("https://chatgbt.one/wp-admin/admin-ajax.php", headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }, data = {
                "_wpnonce": "710ef5f6a3",
                "action": "wpaicg_chat_shortcode_message",
                "message": question + " Accurately answer yes or no with no period or explanation in lowercase. Use sources if needed."
            })
            if ("success" in response.text):
                answer = response.json()["data"]
                tasks[task_key] = {"text": answer}
                questions[question] = answer
                return
        print("[-] AI function exceed 3 retires, exiting...")
        exit(0)         

    def solve_text_questions(self, config, key, job_mode, tasks):
        questions, threads = {}, []
        if (not self.is_answered(tasks, questions)):
            for task_key, question in tasks.items():
                if ("text" not in question):
                    threads.append(threading.Thread(target = self.ask_question, args = (tasks, questions, task_key, question,)))
            
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
        time.sleep(2)
        return self.submit_text_answers(config, key, job_mode, questions, tasks)
    
    def submit_text_answers(self, config, key, job_mode, questions, answers):
        response = self.check_answers(config, key, job_mode, answers)
        response_type = type(response)
        if (response_type == str and response[:2] == "P1"):
            self.write_answers(questions)
            self.previous_answers = self.load_previous_answers()
        elif (response_type == dict):
            self.remove_answers(questions)
        return response