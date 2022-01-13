from Crypto.PublicKey import RSA

def gen_key():
    keyPair = RSA.generate(3072)
    return keyPair

class Person:
        
    def __init__(self):
        keyPair = gen_key()
        self.Public_key = keyPair.publickey().exportKey()
        self.Private_key = keyPair.exportKey()
    
    def generate_public_broadcast(self):
        return self.Public_key

if __name__ == '__main__':
    personA = Person()
    print(personA.Public_key)
    personB = Person()
    print(personB.Public_key)
    personC = Person()



    
