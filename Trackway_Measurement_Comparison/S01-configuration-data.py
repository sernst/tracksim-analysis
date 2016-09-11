import os
import cauldron as cd

SIZE_CLASSES = [
    dict(
        id='t',
        index=0,
        range=(0, 0.25),
        name='Tiny',
        color='rgb(141,211,199)'
    ),
    dict(
        id='s',
        index=1,
        range=(0.25, 0.50),
        name='Small',
        color='rgb(188,128,189)'
    ),
    dict(
        id='m',
        index=2,
        range=(0.5, 0.75),
        name='Medium',
        color='rgb(190,186,218)'
    ),
    dict(
        id='l',
        index=3,
        range=(0.75, 100.0),
        name='Large',
        color='rgb(251,128,114)'
    )
]

ROOT_PATH = os.path.join(
    os.path.expanduser('~'),
    'Dropbox',
    'A16'
)

cd.shared.put(
    SIZE_CLASSES=SIZE_CLASSES,
    ROOT_PATH=ROOT_PATH
)
