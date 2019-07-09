import requests
import subprocess
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import os
vk_session = vk_api.VkApi(token='')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
def main():
    session = requests.Session()
    vk = vk_session.get_api()

    for event in longpoll.listen():
        text = 'try again.'
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
                subprocess.check_output('python3 download_video.py -url {}'.format(event.text),
                                        shell = True)
                vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='video uploaded on server'
                    )
                subprocess.check_output('python3 recognize.py',
                                       shell = True)
                vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='video recognized'
                    )
                text = open('result.txt', 'r', encoding='utf-8').read()
                if len(text) < 4000:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=text)
                else:
                    text_main = text[:int(len(text)/4000)*4000]
                    text_res = text[int(len(text)/4000)*4000:int(len(text)/4000)*4000+int(len(text)%4000)]
                    for i in range(0,len(text_main),4000):
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=text[i:i+4000]
                        )
                    vk.messages.send(user_id=event.user_id,
                        random_id=get_random_id(),
                        message=text_res
                    )
                print('ok')
                os.system('rm samples/*')
                os.system('rm tmp.*')
                os.system('rm current.wav')
                if not text:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='wrong format'
                    )
                    print('no results')
                    continue
        except:
            vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='try again'
                    )

if __name__ == '__main__':
    main()
