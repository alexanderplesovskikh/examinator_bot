import time

import zulip
from db.events import get_pending_events, update_event_with_message_id, get_message_id_from_event, update_event_status


class Worker:
    def __init__(self):
        self.client = zulip.Client(config_file="zuliprc-exerciser-kg")

    def process_events(self):
        while True:
            # Получаем события со статусом 'pending'
            events = get_pending_events()

            for event in events:
                event_id = event['id']
                message_content = event['message_content']
                recipient = event['recipient']
                operation_type = event['operation_type']
                updating_event_id = event['updating_event_id']

                if operation_type == 'send':
                    success, resp = self.send_zulip_message(recipient=recipient, message_content=message_content,
                                                   event_id=event_id)
                elif operation_type == 'update':
                    success, resp = self.update_zulip_message(event_id=event_id, updating_event_id=updating_event_id, new_content=message_content)
                else:
                    print(f'Unknown operation type {operation_type}')
                    continue
                if not success:
                    print(f"Did not do {operation_type} for {event_id}: {type(resp)} {resp}")
                    if isinstance(resp, dict) and resp["code"] == "RATE_LIMIT_HIT":
                        timeout = resp["retry-after"]
                        print(f"Need to slow down for {timeout}")
                        time.sleep(timeout)
                        continue

    def send_zulip_message(self, recipient, message_content, event_id):
        try:
            response = self.client.send_message({
                "type": "private",
                "to": recipient,
                "content": message_content
            })
        except Exception as e:
            print(e)
            return False, e

        if response["result"] == "success":
            message_id = response['id']
            update_event_with_message_id(event_id, message_id)
            update_event_status(event_id, 'sent')
            return True, ""
        else:
            print(response)
            return False, response

    def update_zulip_message(self, event_id, updating_event_id, new_content):
        message_id = get_message_id_from_event(updating_event_id)
        if message_id:
            response = self.client.update_message({
                'message_id': message_id,
                'content': new_content
            })
            if response["result"] == "success":
                update_event_status(event_id, 'sent')
                return True, response
            return False, response
        else:
            reason = f'no message id for event {event_id}'
            return False, reason


if __name__ == '__main__':
    worker = Worker()
    worker.process_events()
