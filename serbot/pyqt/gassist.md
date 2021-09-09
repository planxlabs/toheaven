# popAssist.py Modify (assist method to thread..)
```python
    def __assist(self, rec_request_handler, resp_handler):
        continue_conversation = False
        device_actions_futures = []

        self.conversation_stream.start_recording()
        logging.info('Recording audio request.')
        if rec_request_handler:
            threading.Thread(target=rec_request_handler).start()

        def iter_log_assist_requests():
            try:
                for c in self.gen_assist_requests():
                    assistant_helpers.log_assist_request_without_audio(c)
                    yield c
            except RuntimeError:
                pass
            logging.debug('Reached end of AssistRequest iteration.')

        last_resp = None 
        is_local_device_handler = False

        for resp in self.assistant.Assist(iter_log_assist_requests(), self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.event_type == END_OF_UTTERANCE:
                logging.info('End of audio request detected.')
                logging.info('Stopping recording.')
                self.conversation_stream.stop_recording()
                if last_resp and self.local_device_handler:
                    data = ' '.join(last_resp)
                    data = ' '.join(data.split())
                    is_local_device_handler = self.local_device_handler(data)
            if resp.speech_results: 
                last_resp = [r.transcript for r in resp.speech_results]
            if len(resp.audio_out.audio_data) > 0 and not is_local_device_handler:
                if not self.conversation_stream.playing:
                    self.conversation_stream.stop_recording()
                    self.conversation_stream.start_playback()
                    logging.info('Playing assistant response.')
                self.conversation_stream.write(resp.audio_out.audio_data)
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                logging.debug('Updating conversation state.')
                self.conversation_state = conversation_state
            if resp.dialog_state_out.volume_percentage != 0:
                volume_percentage = resp.dialog_state_out.volume_percentage
                logging.info('Setting volume to %s%%', volume_percentage)
                self.conversation_stream.volume_percentage = volume_percentage
            if resp.dialog_state_out.microphone_mode == DIALOG_FOLLOW_ON:
                continue_conversation = True
                logging.info('Expecting follow-on query from user.')
            elif resp.dialog_state_out.microphone_mode == CLOSE_MICROPHONE:
                continue_conversation = False
            if resp.device_action.device_request_json:
                device_request = json.loads(resp.device_action.device_request_json)
                fs = self.device_handler(device_request)
                if fs:
                    device_actions_futures.extend(fs)
            if self.display and resp.screen_out.data:
                system_browser = browser_helpers.system_browser
                system_browser.display(resp.screen_out.data)
        
        if len(device_actions_futures):
            logging.info('Waiting for device executions to complete.')
            concurrent.futures.wait(device_actions_futures)

        logging.info('Finished playing assistant response.')
        self.conversation_stream.stop_playback()
        
        if resp_handler:
            threading.Thread(target=resp_handler).start()

        return continue_conversation
        
    @retry(reraise=True, stop=stop_after_attempt(3),
           retry=retry_if_exception(is_grpc_error_unavailable))
    def assist(self, rec_request_handler=None, resp_handler=None):
        t = threading.Thread(target=self.__assist, args=(rec_request_handler, resp_handler))
        t.daemon = True
        t.start()
        t.join()        
```

# stt.py
```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QFont
from popAssist import create_conversation_stream
from popAssist import GAssistant

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bl = QLabel('', self)
        self.bl.move(10, 500)
        self.bl.resize(1000, 100)
        self.bl.setFont(QFont('', 80))

        self.bt = QPushButton("Start", self)
        self.bt.move(300, 100)
        self.bt.resize(700, 300)
        self.bt.setFont(QFont('', 100))
        self.bt.clicked.connect(self.onPB)
        
        self.ga = GAssistant(create_conversation_stream(), local_device_handler=self.onAction)

    def onPB(self):
        self.ga.assist(self.onStart, self.onStop)

    def onAction(self, text):
        print("call onAction...")
        self.bl.setText(text)

        return True

    def onStart(self):
        print("call onStart...")
        self.bt.setText("Listen...")  #BUG
 
    def onStop(self):
        print("call onStop")
        self.bt.setText("ReStart")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())
```
