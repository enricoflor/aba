from aba import *
from vform import *
from nform import *


oh3p = [[NForm('sg', 'nom', 'mas') ],  # e-
        [NForm('sg', 'nom', 'neu'),  # ih-
         NForm('sg', 'acc', 'neu'),
         NForm('sg', 'dat', 'neu'),
         NForm('pl', 'dat', 'neu'),
         NForm('sg', 'acc', 'mas'),
         NForm('sg', 'dat', 'mas'),
         NForm('pl', 'dat', 'mas'),
         NForm('sg', 'dat', 'fem'),
         NForm('pl', 'dat', 'fem')],
        [NForm('pl', 'nom', 'neu'),  # s-
         NForm('pl', 'acc', 'neu'),
         NForm('pl', 'nom', 'mas'),
         NForm('pl', 'acc', 'mas'),
         NForm('sg', 'nom', 'fem'),
         NForm('pl', 'nom', 'fem'),
         NForm('sg', 'acc', 'fem'),
         NForm('pl', 'acc', 'fem')]]


mgerm3p = [[NForm('sg', 'nom', 'neu'), # e-
            NForm('sg', 'acc', 'neu'),
            NForm('sg', 'nom', 'mas')],
           [NForm('sg', 'dat', 'neu'),  # ih-
            NForm('pl', 'dat', 'neu'),
            NForm('sg', 'acc', 'mas'),
            NForm('sg', 'dat', 'mas'),
            NForm('pl', 'dat', 'mas'),
            NForm('sg', 'dat', 'fem'),
            NForm('pl', 'dat', 'fem')],
           [NForm('pl', 'nom', 'neu'),  # s-
            NForm('pl', 'acc', 'neu'),
            NForm('pl', 'nom', 'mas'),
            NForm('pl', 'acc', 'mas'),
            NForm('sg', 'nom', 'fem'),
            NForm('pl', 'nom', 'fem'),
            NForm('sg', 'acc', 'fem'),
            NForm('pl', 'acc', 'fem')]]

middledutch3p = [[NForm('sg', 'nom', 'neu'), # h-
                  NForm('sg', 'acc', 'neu'),
                  NForm('sg', 'dat', 'neu'),
                  NForm('sg', 'nom', 'mas'),
                  NForm('sg', 'acc', 'mas'),
                  NForm('sg', 'dat', 'mas'),
                  NForm('sg', 'acc', 'fem'),
                  NForm('sg', 'dat', 'fem'),
                  NForm('pl', 'acc', 'neu'),
                  NForm('pl', 'acc', 'mas'),
                  NForm('pl', 'acc', 'fem'),
                  NForm('pl', 'dat', 'neu'),
                  NForm('pl', 'dat', 'mas'),
                  NForm('pl', 'dat', 'fem')],
                 [NForm('pl', 'nom', 'neu'), # z-
                  NForm('pl', 'nom', 'mas'),
                  NForm('pl', 'nom', 'fem'),
                  NForm('sg', 'nom', 'fem')]]

eastfrisian3p = [[NForm('sg', 'nom', 'mas'), #h-
                  NForm('sg', 'acc', 'mas'),
                  NForm('sg', 'dat', 'mas'),
                  NForm('sg', 'acc', 'fem'),
                  NForm('sg', 'dat', 'fem'),
                  NForm('pl', 'acc', 'neu'),
                  NForm('pl', 'acc', 'mas'),
                  NForm('pl', 'acc', 'fem'),
                  NForm('pl', 'dat', 'neu'),
                  NForm('pl', 'dat', 'mas'),
                  NForm('pl', 'dat', 'fem')],
                 [NForm('sg', 'nom', 'neu'), # d-
                  NForm('sg', 'acc', 'neu'),
                  NForm('sg', 'dat', 'neu')],
                 [NForm('pl', 'nom', 'neu'), # z-
                  NForm('pl', 'nom', 'mas'),
                  NForm('pl', 'nom', 'fem'),
                  NForm('sg', 'nom', 'fem')]]

afrikaans3p = [[NForm('sg', 'nom', 'mas'), #h-
                NForm('sg', 'acc', 'mas'),
                NForm('sg', 'dat', 'mas'),
                NForm('sg', 'acc', 'fem'),
                NForm('sg', 'dat', 'fem'),
                NForm('pl', 'nom', 'neu'),
                NForm('pl', 'nom', 'mas'),
                NForm('pl', 'nom', 'fem'),
                NForm('pl', 'acc', 'neu'),
                NForm('pl', 'acc', 'mas'),
                NForm('pl', 'acc', 'fem'),
                NForm('pl', 'dat', 'neu'),
                NForm('pl', 'dat', 'mas'),
                NForm('pl', 'dat', 'fem')],
               [NForm('sg', 'nom', 'neu'), # d-
                NForm('sg', 'acc', 'neu'),
                NForm('sg', 'dat', 'neu')],
               [NForm('sg', 'nom', 'fem')]] # z-

oldicelandic3p = [[NForm('sg', 'nom', 'mas'), #h-
                   NForm('sg', 'acc', 'mas'),
                   NForm('sg', 'dat', 'mas'),
                   NForm('sg', 'nom', 'fem'),
                   NForm('sg', 'acc', 'fem'),
                   NForm('sg', 'dat', 'fem')],
                  [NForm('sg', 'nom', 'neu'), # th-
                   NForm('sg', 'acc', 'neu'),
                   NForm('sg', 'dat', 'neu'),
                   NForm('pl', 'nom', 'neu'),
                   NForm('pl', 'nom', 'mas'),
                   NForm('pl', 'nom', 'fem'),
                   NForm('pl', 'acc', 'neu'),
                   NForm('pl', 'acc', 'mas'),
                   NForm('pl', 'acc', 'fem'),
                   NForm('pl', 'dat', 'neu'),
                   NForm('pl', 'dat', 'mas'),
                   NForm('pl', 'dat', 'fem')]]
