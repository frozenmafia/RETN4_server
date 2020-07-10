from random import randint
import json
import os


class OTP_MANAGER():



    def __init__(self):
        self.otp = randint(100000,999999)
        # memory = self.readFile()
        # new_memory = memory + [
        #     {
        #         "phone":phone,
        #         "otp_generated":otp
        #     }
        # ]
        # self.writeFile(new_memory)


    def get_cwd(self):
        return os.path.dirname(os.path.abspath(__file__))


    def get_otp(self):
        return self.otp

    def writeFile(self,data_list):
        file_to_be_written = {
            "otp_memory":data_list
            }
        file_path = self.get_cwd()+"/otp_memory.json"
        with open(file_path,'w+',encoding='utf-8') as f:
            json.dump(file_to_be_written,f,indent=4)
        f.close()

    def readFile(self):
        file_path = self.get_cwd()+"/otp_memory.json"
        with open(file_path) as f:
            data=json.load(f)
        f.close()
        return data["otp_memory"]

    