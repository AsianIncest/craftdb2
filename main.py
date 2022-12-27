from mctop import Agregator_mctop
from topcraft import Agregator_topcraft

if __name__ == "__main__":
    mctop = Agregator_mctop()
    mctop.start()

    topcraft = Agregator_topcraft()
    topcraft.start()


