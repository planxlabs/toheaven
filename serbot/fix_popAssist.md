> {python3_lib_path}/popAssist.py > class GAssistant >  assist Method

## Modify
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
