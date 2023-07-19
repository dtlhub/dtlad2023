#!/usr/bin/env python3

import os
import sys
import json
import time
import logging
import threading
import socketserver
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from msngr import Messanger


class Servant:
    def __init__(self):
        self.before_input = "welcom to mesfnasensgetR! on SANbKA!!\n"
        self.msngr = Messanger()

    def serve(self, input_data):
        if "option" not in input_data.keys():
            return {"error": "you must specify option"}
        options = {
            'login': [self.msngr.login, ['login', 'token']],
            'register': [self.msngr.register, ['login', 'hello_message', 'secret_message']],
            'get_hello_message': [self.msngr.get_hello_message, []],
            'get_secret_message': [self.msngr.get_secret_message, []],
            'list_users': [self.msngr.list_users, []],
            'init_key_exchange': [self.msngr.init_key_exchange, ['generator', 'modulus']],
            'communicate_dh_feistel': [self.msngr.communicate_dh_feistel, ['friend']],
            'communicate_ask_to_encrypt': [
                self.msngr.communicate_ask_to_encrypt,
                ['data', 'friend'],
            ],
            'communicate_ask_for_secret': [self.msngr.communicate_ask_for_secret, ['friend']],
            'decrypt': [self.msngr.decrypt, ['ciphertext', 'key']],
        }
        option = options[input_data['option']]
        func = option[0]
        params = [input_data[i] for i in option[1]]
        return func(*params)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def log(self, msg):
        remote_ip = self.client_address[0]
        logging.info(f"{remote_ip}::{msg}")

    def recvline(self):
        buf = b""
        while not buf.endswith(b"\n"):
            buf += self.request.recv(1)
        return buf

    def send_msg(self, msg):
        jsonified = (json.dumps(msg) + '\n').encode()
        try:
            self.request.sendall(jsonified)
        except BrokenPipeError:
            pass

    def handle(self):
        self.log("connected")

        c = Servant()
        max_recv_size = 1024
        if hasattr(c, 'max_payload_size'):
            max_recv_size = c.max_payload_size
        if hasattr(c, 'timeout_secs'):
            time_started = time.time()

        while True:
            if hasattr(c, 'timeout_secs') and time.time() > time_started + c.timeout_secs:
                msg = {"error": "Out of time"}
                self.send_msg(msg)
                break

            if hasattr(c, 'no_prompt'):
                del c.no_prompt
                data = {}
            else:
                if hasattr(c, 'before_input'):
                    try:
                        self.request.sendall(c.before_input.encode())
                    except BrokenPipeError:
                        break
                    del c.before_input

                if hasattr(c, 'max_payload_size'):
                    try:
                        self.data = b""
                        while len(self.data) < max_recv_size:
                            chunk = self.request.recv(1024)
                            if not chunk:
                                break
                            self.data += chunk.strip()
                            if b"\n" in chunk:
                                break
                    except ConnectionResetError:
                        break
                else:
                    try:
                        self.data = self.request.recv(max_recv_size).strip()
                    except ConnectionResetError:
                        break
                if len(self.data) >= max_recv_size:
                    msg = {"error": f"You may send up to {max_recv_size} bytes per message."}
                    self.send_msg(msg)
                    break
                if self.data:
                    self.log(self.data)
                try:
                    data = json.loads(self.data)
                except json.decoder.JSONDecodeError:
                    if b"'" in self.data:
                        msg = {
                            "error": "Invalid JSON. Remember to surround strings with double quotes rather than single quotes."
                        }
                    else:
                        msg = {"error": "Invalid JSON"}
                    self.send_msg(msg)
                    break
            try:
                out = c.serve(data)
                if hasattr(c, 'before_send'):
                    self.request.sendall(c.before_send.encode())
                    del c.before_send
                if isinstance(out, list):
                    for obj in out:
                        self.send_msg(obj)
                elif out is None:
                    pass
                else:
                    self.send_msg(out)
                if hasattr(c, 'exit'):
                    break
            except Exception as e:
                error = getattr(e, 'message', repr(e))
                msg = {"error": "Exception thrown", "exception": error}
                self.send_msg(msg)
                self.log(error)
                break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def start_server(port=0):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(
        handlers=[
            RotatingFileHandler('logs/msngr.log', maxBytes=50 * 1024 * 1024, backupCount=3),
            StreamHandler(sys.stdout),
        ],
        level=logging.INFO,
        format='%(asctime)s::msngr::%(message)s',
    )
    with ThreadedTCPServer(('0.0.0.0', port), ThreadedTCPRequestHandler) as server:
        logging.info(f"Starting up on port {port}")
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        while True:
            time.sleep(10)

        server_thread.join()


def main():
    start_server(8441)


if __name__ == "__main__":
    main()
