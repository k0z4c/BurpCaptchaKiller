from burp import (
  IBurpExtender,
  IIntruderPayloadGeneratorFactory,
  IIntruderPayloadGenerator,
  IIntruderAttack
)

from java.io import PrintWriter

import pytesseract

# https://pypi.org/project/pytesseract/
# python3-imaging
# https://github.com/tesseract-ocr/tesseract
try:
  from PIL import Image
except ImportError:
  import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sondrioma\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# https://github.com/PortSwigger/burp-extender-api/blob/master/src/main/java/burp/IIntruderPayloadGeneratorFactory.java
# https://github.com/PortSwigger/burp-extender-api/blob/master/src/main/java/burp/IIntruderPayloadGenerator.java

    
class BurpExtender(IBurpExtender):

  def registerExtenderCallbacks(self, callbacks):
    callbacks.setExtensionName ("Captcha Killah")
    helpers = callbacks.getHelpers()
    
    class IntruderPayloadGeneratorFactory(IIntruderPayloadGeneratorFactory):
      def getGeneratorName(self):
        return "Captcha Killah"
    
      def createNewInstance(attack):
        return IntruderPayloadGenerator()
    
    class IntruderPayloadGenerator(IIntruderPayloadGenerator):
      MAX_REQUESTS = 10
      number_of_requests = 0
  
      def hasMorePayloads(self):
        return number_of_requests < MAX_REQUESTS
  
      def getNextPayload(self, baseValue):
        captcha_url = ''
        captcha = requests.get(captcha_url).content

        try:
          solution = pytesseract.image_to_string(captcha)
        except RunTimeError as timeout_error:
          pass
      
        stdout = PrintWriter(callbacks.getStdout(), True)
        stdout.println(solution)
        return bytearray(solution)
    
      def reset(self):
        pass
    
    callbacks.registerIntruderPayloadGeneratorFactory(IntruderPayloadGeneratorFactory())
    
    return
