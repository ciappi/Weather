from kivy.gesture import GestureDatabase, Gesture
from kivy.uix.boxlayout import BoxLayout


gesture_strings = {
    'left_to_right_line': 'eNp91HtMFEccwPHjIcj5oqJUrcopPg6qiNYWalVGKwxSH6ioKxbhHit7Pby7390ucGl+eiiiTZrURNtoG5UmJUajhj8MicEg0WgM2mpqtNGY+Ih/YExT4h+WRBM7O5nVZjC7f+xtvveZ2b293Umk+IKBxnhBvRrTjajqpOITHHktkISQ7FaGORyOpoBf1yCFkp0Rh7kp6WwX06PhoBqD1BoY9t5ZNnDghDQ2VzrCcLcy0hzmi6pqKBIOhPQYZNSA002Jv5dPS4lB+EEbjKBEdchxJCXaIzmOoiRYJ8fRlISGDB9DSSRixUoRMymBt2fn8yS1wQeUxFxyHEuJfkCOWZQ0DpHjKGlql+N4SuI5b8ztf2fPpuTbIb/oQ0qQyHECJbuOW8OtOJGSRLkl5/Fv22ASJS0TrJgp5Ecsvr14h7ikySwOiqgPCDmFkt2dVrwp5pzKYr8Ve4XMoWRPsRU7xZwuFiut2C7kNBbr5DidxcNyzGWxU44zWOyX40xKWofLcRaLLjnOZrFcjuypa1XkmMfikOvMZ1GT48eqksYOxGM8pwbmut/7DlSawAkF7BWYh1DoVpLYqDjMpyUtC6e/yvqb8NAMC+jFp7t6+x4VNhhezdSfICx0a++cxsSTqo5Xl2m6EJ8ifGYvihCKZfE4tbgjPfuUEJ8jLJLFw9IXWc88tUJ8gbCYi73aucxfq3pN8YDk3Qj2DAixBGGpvShBIFx8d7R0VsEFLu7hqZ/KXrwWYhnCclncPdL2l9HdJ8SXCCvsRSlCmSxuH+z5YXBitRAUoVwWtyrOFE1r14VYiVBhL75CWCWLvrLE7//MPCDEaoQ18v24/O+Jub84iRBrESrtxTqE9fL/0vlHof90db8QGxCq7MVGhE32YjOCIotDL/d2HB1MCLEFoVoSJWeac+IDWy2xFeFre1GDsM1e1CLUcRF/k3t91AiHKbqOHb/iWWs9QR4ELxfeLT3Pzt7n4tKM7o6uiHXHfAh+e6EibOfC3XSy6OAtLq5mp5x8nqQIUY+gmeJi8ztx8/uKSYF8SwQQvrEXQYQGLlp/e3n1aVfCFH8mj3WdOFcoxA6EEBf77+17EJ3K78ftH6/tv9CdKkQYISKLOw3XkvMPVxle1fB6lDFs0RArTW0kGvYbPh2AkoyzezyNablKBvtaDzeoUU/Ip0KUlpw/Ym4/8zVLUwP1mg4xStx8MXMpqWwf8uxQQecrIhiGt+A/gxOtAA==',
    'right_to_left_line': 'eNp91mtQlFUYwPFFEQRJV7Mk09wwZLUkUKzElJNRp9CUhHC9gLCwssRl99kLNzmyXKQsL1uoCQLR0AcvU8MYgzWFi5UUDDKrGcJ0Ybs4w6iTTJ/SGYeefTvLMM867Ydl57f/8+6755x3XxxTs/Pzisuicw1Wm91iCOXyL6iWVkGAgClaXYhKpbKZCgyWrKJsA0zlCV80eB+Numn4Rklejs0IgZztVau8D90sfJIH22W2mHLs2TaYxlnw2Xmu6ohEXRC+bTTk5RptEMRZhOq/QcH4ZLVZTPkGKwSnw/T7nlOKEoRCCJ5ZqIAZWl2Yd1i2xWAoMpvyimxWCEuHB7Sc7RtVDsuZxa28qIOZiB4fdkuchfi5D9slqhGdPmyVOBtR50OnxDmc1XZTfBDRTHEuoobiQ5zVlFJ8GFFLcR5n1W6K4YiM4iOI0ynO56zKSfFRRB39mgs4c7gpLkR00ll6DFFHcRGiik6yhrPKdoqPIybTNYpAnBiuLFZAHSzGndVO8QnEzePeB+KYHB6JODHch0s4E5k+VEaM10EUorJbAyYhbpsKN8WliE46fBliMsUnEVV0+FOc7Wmn5XJEv+HRnJW3Unwa0a+MQfT7mrGclXXTWVqBaKa4EjGGznwcZ6V+V8cqRAdd4mc4K+mm+CxiMt02z3FW3EpxNSKjGM+Z3UNxDWIMxec5s/ntz7WIDorrEFUUEziztlNkiBqKL0xMziRcj6/9PuhFzsBDJyQR0Unn8yVENZ35lzkze+gacUS/Pf8KYibFVxEZ3QxJiBqKGxD9ts1Gzkwj9Dp6DVFFd90mzoocFDdzVuj7dKtaDk/mrMBD8XXESvlBE7gFUUPLFETfdTSBqZzl+x3zDcRWimmIDjp862TUSNQZlHuRvHFsS4ft2vvedZK9QSjswJvOTgHpWl0AjiqDDJ6wfHZI/0CmSoFS2MUT/ph7cedY33W73uitMwVkaY0Z3OWoP3fs0jWVEYvffl916si5LlnoBWTTwtPSfLe8rUYWOQIMtBgZbUpaGHteFrsF5NLip+8/2RJ+21cYBeT9f/GmgHxaDN3LCLz1TZAsCgQU0mLw+LqWuKZOWRQJMNHix1MDw+6DA7IwCwBa/HB6ZNuBwl9lYRFgVYrSNth0ItLhLdxlmZG34ntkYRNgVwrzIqupsVk5xsDl7qvhKRWyKBZQohQZhYPrjalK0RdcHXQy6GdZlAoo8xa+9fMW382PuDA+FCiLcgF7lALGasNya5Xi66HFVyrr/5RFhQChFOW2qpvGGcqZdnXsb/vrpFoWewVU0qKzd0PG+dU6WTgEVNHi0zONJWtqk2VRLaCGFg1L1t7tuOiQRa2AfUqhHw7bfukf75m6LC03eFy6r6gT8BaZD9dH8cOHo8o1snhbwH4yp66zsTf0tjTfmb4j4F2yLq4ve3Lvpd5ulcUBAQdpcWHuZyuSTo/K4pCAw7T4dsqc4r+Hv5KFU8B7tOhVw8odyz6WxfsC6mnR3xeTeHM3k8URAUfpd7k8c2tp5C8dsjgm4AOy+q4rvVEhcEcvi+MCGuicXk0YPNOj7pdFo4ATZF1cgws64w5FN8qiSUCzUlRVJFyPS1KOce3O0a60jUa73mDXZ+kC8UejKKvQAC3Kv1HwoV0f/S8wgMTI',
    'bottom_to_top_line': 'eNp91FtMFFcYwPFFEWWLYq2KrW3BGyyCSC0VCuiO11m0Kmi3jgrIXgZ2i+7utzsLC+0nIyYbbGpcE2OsTeMaHzCWpBdf1KaBRCov3ogajZcoiYkxMS32qQ1p6ZnjOclphuw8zEz+8ztzzmQyo0/2tPrbOkpa1IgWDatWmR3BUngQ0hAm2ZRMi8WiBfepYVfAo8Jk2X7pG2M7pUwhF9r9Xs0H6bKUb6Gbkk127GZ7Q+GgN+rRYIosZWbv/M7ZvU7JIJd9qr/Fp0GGLHUmXg+aSnYRLRxsVSMwtQGmTbimHRRYIZOszIrwhk3JMoZ5wqoaCAX9AS0CWQ0w3SZL0VF6W1naYx83tjjMkKU2C4/0OCkO2WIcZ3KmEF1dLL4pRE/SOKbFYZYQm3UW3xKiX6IncZgtxFY+0RwhBvhEc4UYamLDc4QIOovzSJRYjCRZfJvEWhY1Ht8hMcTi6xOyzvlCbM9j8l0xPmXxPSHGEiy+L8SOXLb4XDHeYjJPiJ38iRaQqPP4Bxu+kMQEi1/OZHIRiUke+RMtFiLy2ZeIka8zX4yjLBYI8QC/p02MXBYKses0m2ipGLksEqI+j8ViMSosLhNjiMUSMfJXvFyMPSyWivEkix+IkT/RCjGeY/FDlX6C7Hspa4CPbBN+bLUGsMJK8q2VI1TYlDQyqgM+lvufOQqGT2z5moYYVMr9x+wzjpTJlqjbZ+gqhGqbj7iRP0/P6S1a6SPiSN+BH0oPS0ysQlidWtgRJCqenn+VVlzzu1msQVhLxeMnFUsctV6zWIewPrXYgLCRigdH51cduz7XLGQER2pRg7CJinur/617WHPVLDYjfELFnaqxrfc3DprFFoStqcU2hFoqhuOzVvQMZplFHcJ2Kq4ntxeHu/vMYgfCp1RccY/0fBsLGUK7Zk1PvuRvzonwWWqxE0FJLXYh7Kbi14XxyqvPJUM0152qdw1ysQehnope57aX5d/rRNibqpR/Gt1cNCA0phZ7EZqoOF548atfqpNm4UJwG8J+sGvsVeHABPfwIHipOJMMn12MTWahIjRT0RfLme3uKTWLFgQfFZcdOSdWkVdkEn6Ez6nov/DixiNnwhAw8MKZW6kz0Yqwj4rfNgzlTS+tMMQX3vyio+u52I8QoGJo7Mfq+p9HDdF96Cd9vJfPEkQIUXFNLxsYKQ+ZBSCEqbh1s+1wc6PDLCIIGhXDifJNBbnTzCKK0EbF7b8zuq4smGCWdoQYFXeHzjz/a5H0P6FG3S4lnfw0Aq79KnTQ3yF0Rt0l/wF15t2j'
}

gestures = GestureDatabase()
for name, gesture_string in gesture_strings.items():
    gesture = gestures.str_to_gesture(gesture_string)
    gesture.name = name
    gestures.add_gesture(gesture)


class GestureBox(BoxLayout):

    def __init__(self, **kargs):
        for name in gesture_strings:
            self.register_event_type('on_{}'.format(name))
        super(GestureBox, self).__init__(**kargs)

    def on_left_to_right_line(self):
        pass
        
    def on_right_to_left_line(self):
        pass

    def on_bottom_to_top_line(self):
        pass

    def on_touch_down(self, touch):
        touch.ud['gesture_path'] = [(touch.x, touch.y)]
        super(GestureBox, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        touch.ud['gesture_path'].append((touch.x, touch.y))
        super(GestureBox, self).on_touch_move(touch)
        
    def on_touch_up(self, touch):
        if 'gesture_path' in touch.ud:
            gesture = Gesture()
            gesture.add_stroke(touch.ud['gesture_path'])
            gesture.normalize()
            match = gestures.find(gesture, minscore=0.90)
            if match:
                self.dispatch('on_{}'.format(match[1].name))
        super(GestureBox, self).on_touch_up(touch)
