import socket
import json
import binascii
from Crypto.Cipher import AES

class Device:
    _model = ''
    _sid = ''

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, value):
        self._sid = value


class Gateway:
    def __init__(self, ip='auto', sid='', gwpasswd='', token=''):
        self.aes_key_iv = bytes([0x17, 0x99, 0x6d, 0x09, 0x3d, 0x28, 0xdd, 0xb3, 0xba, 0x69, 0x5a, 0x2e, 0x6f, 0x58, 0x56, 0x2e])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.multicast = ('224.0.0.50', 4321)
        if ip == 'auto':
            gateway = self.whois()
            self.unicast = (gateway.get('ip'), int(gateway.get('port')))
            self.sid = gateway.get('sid')
        else:
            self.unicast = (ip, 9898)
            self.sid = sid
        self.gwpasswd = gwpasswd
        self._token = token

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def whois(self):
        """Discover the gateway device multicast (IP: 224.0.0.50 peer_port: 4321 protocal: UDP)"""

        return self._send_multicast(cmd='whois')

    def get_device_list(self):
        """The command is sent via unicast to the UDP 9898 port of the gateway,
        which is used to obtain the sub-devices in the gateway."""

        return self._send_unicast(cmd='discovery')

    def get_id_list(self):
        return self._send_unicast(cmd='get_id_list')

    def read_device(self, sid):
        """Reading devices
        Send the "read" command via unicast to the gateway's UDP 9898 port.
        Users can take the initiative to read the attribute status of each device,
        and the gateway returns all the attribute information associated with the device."""

        return self._send_unicast(cmd='read', sid=sid)

    def write_device(self, model, sid, short_id, data):
        """Send the "write" command via unicast to the gateway's UDP 9898 port.
        When users need to control the device, the user can use the "write" command."""
        _data = data
        _data['key'] = self.get_key().decode()
        return self._send_unicast(cmd='write',
                                  model=model,
                                  sid=sid,
                                  short_id=short_id,
                                  data=data)

    def read_all_devices(self):
        id_list = self.get_id_list()
        id_list = json.loads(id_list.get('data'))
        ret = []
        for _id in id_list:
            ret.append(self.read_device(_id))
        return ret

    def _cmd(self, args):
        print(args)
        return json.dumps(args)

    def _answer(self):
        data_bytes, addr = self.sock.recvfrom(1024)
        if data_bytes:
            return json.loads(data_bytes.decode())
        else:
            return ''

    def _send_multicast(self, **kwargs):
        self.sock.sendto(self._cmd(kwargs).encode(), self.multicast)
        return self._answer()

    def _send_unicast(self, **kwargs):
        self.sock.sendto(self._cmd(kwargs).encode('ascii'), self.unicast)
        return self._answer()

    def refresh_token(self):
        self._token = self.get_id_list().get('token')

    def get_key(self):
        """Get current gateway key"""
        cipher = AES.new(self.gwpasswd, AES.MODE_CBC, self.aes_key_iv)
        self.refresh_token()
        encrypted = cipher.encrypt(self.token)
        return binascii.hexlify(encrypted)

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    gw = Gateway(gwpasswd='cjvt7wr3q7df72rq')
    print(gw.whois())
    # print(gw.get_id_list())
    print(gw.get_device_list())
    print(gw.read_all_devices())
    gw.refresh_token()
    devs = gw.read_all_devices()
    print(gw.write_device(model="ctrl_neutral2",
                          sid="158d00029b1929",
                          short_id=44507,
                          data={"channel_1": "off"}))
    print(gw.token)