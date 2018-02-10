from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import socket


class BaseWindows(BoxLayout):

    temp = ObjectProperty()
    hum = ObjectProperty()
    press = ObjectProperty()

    def get_bme_value(self, dt):
        s = socket.socket()
        s.connect(('192.168.3.1', 9090))
        s.send(b'bme')
        self.parse_bme_val(s.recv(30))
        s.close()

    def parse_bme_val(self, data):
        raw_value = str(data, 'utf8').split('|')
        self.temp.text = 'Температура: ' + raw_value[0]
        self.hum.text = 'Влажность: ' + raw_value[1]
        self.press.text = 'Давление: ' + raw_value[2]



class RequestApp(App):
    def build(self):
        clock = BaseWindows()
        Clock.schedule_interval(clock.get_bme_value, 1)
        return clock


if __name__ == '__main__':
    RequestApp().run()