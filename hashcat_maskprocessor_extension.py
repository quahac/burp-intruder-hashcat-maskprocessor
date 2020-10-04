from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from burp import IIntruderPayloadProcessor


''' Lines  8 up to 120  Credits to the original coder https://github.com/Xvezda/python-maskprocessor edited a little bit code to fit Burp Extension '''
import sys
import string
from itertools import product

charset_l = string.ascii_lowercase
charset_u = string.ascii_uppercase
charset_d = string.digits
charset_s = ' ' + string.punctuation
charset_a = charset_l + charset_u + charset_d + charset_s
charset_b = ''.join([chr(v) for v in range(0x00, 0xff+1)])


charset_1 = ''
charset_2 = ''
charset_3 = ''
charset_4 = ''


def expand(mask):
    if not mask:
        return []
    charsets = []
    it = iter(mask)
    while True:
        try:
            c = next(it)
        except StopIteration:
            break
        if c == '?':
            try:
                c2 = next(it)
            except StopIteration:
                break
            if c2 == 'l':
                charsets += [charset_l]
            elif c2 == 'u':
                charsets += [charset_u]
            elif c2 == 'd':
                charsets += [charset_d]
            elif c2 == 's':
                charsets += [charset_s]
            elif c2 == 'a':
                charsets += [charset_a]
            elif c2 == 'b':
                charsets += [charset_b]
            elif c2 == '1':
                charsets += [charset_1]
            elif c2 == '2':
                charsets += [charset_2]
            elif c2 == '3':
                charsets += [charset_3]
            elif c2 == '4':
                charsets += [charset_4]
            elif c2 == '?':
                charsets += ['?']
            else:
                raise SyntaxError("invalid character '%s'" % (c2,))
        else:
            charsets += [c]
    return charsets


def maskprocessor(mask,
                  custom_charset1=None,
                  custom_charset2=None,
                  custom_charset3=None,
                  custom_charset4=None):

    charsets = []

    global charset_1, charset_2, charset_3, charset_4

    charset_1 = ''.join(expand(custom_charset1))
    charset_2 = ''.join(expand(custom_charset2))
    charset_3 = ''.join(expand(custom_charset3))
    charset_4 = ''.join(expand(custom_charset4))

    charsets = expand(mask)
    for result in product(*charsets):
        yield ''.join(result)


def mask_main(arg1):
    import argparse
    from textwrap import dedent
    spl1 = arg1.split()
    spl1.insert(0, '')

    sys.argv= spl1
    parser = argparse.ArgumentParser(
        'maskprocessor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent(""),
        epilog=dedent(""))
    parser.add_argument('mask', type=str)
    custom_charset_group = parser.add_argument_group()
    custom_charset_group.add_argument('--custom-charset1', '-1', type=str, metavar='CS')
    custom_charset_group.add_argument('--custom-charset2', '-2', type=str, metavar='CS')
    custom_charset_group.add_argument('--custom-charset3', '-3', type=str, metavar='CS')
    custom_charset_group.add_argument('--custom-charset4', '-4', type=str, metavar='CS')
   
     
    args = parser.parse_args()
    global i
    i = maskprocessor(args.mask,
                           custom_charset1=args.custom_charset1,
                           custom_charset2=args.custom_charset2,
                           custom_charset3=args.custom_charset3,
                           custom_charset4=args.custom_charset4)

 


class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory, IIntruderPayloadProcessor):
    def registerExtenderCallbacks(self, callbacks):
        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()

        # set our extension name
        callbacks.setExtensionName("Hashcat Maskprocessor")

        # register ourselves as an Intruder payload generator
        callbacks.registerIntruderPayloadGeneratorFactory(self)

        # register ourselves as an Intruder payload processor
        callbacks.registerIntruderPayloadProcessor(self)

    def getGeneratorName(self):
        return "hashcat maskprocessor"

    def createNewInstance(self, attack):
        return IntruderPayloadGenerator()

    def getProcessorName(self):
        return "Not Implemented"

    def processPayload(self, currentPayload, originalPayload, baseValue):
        print "ProcessPayload Not Implemented"
        pass



class IntruderPayloadGenerator(IIntruderPayloadGenerator):
    
    
    def __init__(self):
        global x
        x = 0
        pass

    def hasMorePayloads(self):
        return True

    def getNextPayload(self, baseValue):
        global x
        if x == 0:
          mask_main(str(bytearray(baseValue)))
          x = x + 1
        try:
          return (next(i))
        except StopIteration:
          return 

    def reset(self):
        return

