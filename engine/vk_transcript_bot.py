import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import os
from engine.download_video import download_video
from engine.recognize import *
from engine.process_rus import reformat_rus

vk_session = vk_api.VkApi(token='804a96abaf394ad8c55d7d472e3ea799fade274030c7927af4936798f676938ce9d4cd5130c6ab6b50df8')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def video2text(video, vk, event):
    start = time.time()
    get_audio(video)
    split_into_frames('current.wav')
    files = sorted(glob('engine/samples/*.wav'))
    print(files)
    open('result.txt', 'w', encoding='utf-8').write('')

    cnt = 0
    for file in files:
        print(file)
        recognize(file)
        cnt += 1
        processed = round(float(cnt/len(files))*100,2)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f'{processed}% processed'
        )
    end = time.time()
    print('elapsed time: {}'.format(end - start))


def main():
    session = requests.Session()
    vk = vk_session.get_api()

    for event in longpoll.listen():
        text = 'try again.'
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                os.system('rm engine/samples/*')
                print('id{}: "{}"'.format(event.user_id, event.text))
                if 'https' not in event.text:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='unexpected input'
                    )
                    continue
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='uploading began'
                )
                download_video('engine/tmp', event.text)
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='video uploaded on server'
                )
                video2text('engine/tmp*', vk, event)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='video recognized'
                )

                with open('engine/result.txt', 'r', encoding='utf-8') as f:
                    text = f.read().replace('..','.').replace('. .','.')
                if len(text) < 4000:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=text)
                else:
                    text_main = text[:int(len(text) / 4000) * 4000]
                    text_res = text[int(len(text) / 4000) * 4000:int(len(text) / 4000) * 4000 + int(len(text) % 4000)]
                    for i in range(0, len(text_main), 4000):
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=text[i:i + 4000]
                        )
                    vk.messages.send(user_id=event.user_id,
                                     random_id=get_random_id(),
                                     message=text_res
                                     )
                print('ok')
                os.system('rm engine/samples/*')
                os.system('rm engine/tmp.*')
                os.system('rm engine/current.wav')
                os.system('rm engine/result.txt')
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
