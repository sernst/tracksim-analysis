import os
import cauldron as cd


# The name of the trackway to load for the analysis, which
# can optionally be supplied from the command line when
# running in production
cd.shared.TRACKWAY_NAME = cd.shared.fetch(
    'trackway_name',
    'BEB-515-2009-1-S-18'
)

# The location on disk where the A16 Cadence databases are stored,
# which will be used to load the data for the trackway for analysis
cd.shared.ROOT_PATH = os.path.join(
    os.path.expanduser('~'),
    'Dropbox',
    'A16'
)

