from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'junior_2_sleep'
        self.triggers = '158d00033ef2d8.status.long_click_press'
        self.place = 'Bedroom'
    
    def on(self):
        dev_to_off = ['158d00024e2e5b', '158d00027d0065', '158d000283b219',
                      '158d00029b1929', '158d0002a16338', '158d0002a18c2b', '158d0002abac97',
                      '158d0002bffe5a', 'rgb01', '0x0000000007e7bae0']
        lamp = self.get_device('235444403')
        lamp.on()
        lamp.set_bricct(100,1)
        for _sid in dev_to_off:
            dev = self.get_device(_sid)
            if dev.model == 'plug':
                dev.power.off()
            elif dev.model == 'ctrl_neutral2':
                dev.channel_0.off()
                dev.channel_1.off()
            elif dev.model == 'ctrl_neutral1':
                dev.channel_0.off()
            elif dev.model in ('bslamp1', 'color', 'rgbstrip', 'bravia'):
                dev.off()
        self.sleep(10)
        lamp.set_bricct(1,1)