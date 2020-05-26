from .base import Dummy
from . import Drivers
from pyiot.xiaomi.aqara import *
import json
from datetime import datetime


class GatewayInstance:
    # not thread sefe 
    gateway = None
    def __new__(cls, daemon):
        if GatewayInstance.gateway is None:
            GatewayInstance.gateway = Gateway(gwpasswd=daemon.config['gateway']['password'])
            GatewayInstance.gateway.watcher.add_report_handler(daemon.bus.emit_cmd)
        return GatewayInstance.gateway
        

class Driver:
    
    def __new__(cls, data, daemon):
        gw = GatewayInstance(daemon)
        dev = {
            'ctrl_neutral1': CtrlNeutral,
            'ctrl_neutral2': CtrlNeutral2,
            'sensor_ht': SensorHt,
            'weather.v1': WeatherV1,
            'magnet': Magnet,
            'sensor_motion.aq2': SensorMotionAq2,
            'sensor_switch.aq2': SensorSwitchAq2,
            'plug': Plug,
            'switch': Switch,
            'gateway': cls.get_gateway}.get(data['model'], Dummy)(sid=data['sid'], gateway=gw)
        daemon.bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        return dev
    
    @classmethod
    def get_gateway(cls, **kwargs):
        return kwargs['gateway']