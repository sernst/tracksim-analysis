import cauldron as cd
from collections import namedtuple

CSV_COLUMN = namedtuple('CSV_COLUMN', ['index', 'name', 'fill'])

csv_columns = [
    # Row index within the spreadsheet file where the entry is found. This
    # value can change any time a new import process occurs and represents the
    # location in the most recent spreadsheet file. It should only be used for
    # reference given that the value can arbitrarily change.
    CSV_COLUMN(0, 'index', None),

    # The short name of the track site where the print resides, e.g. BEB.
    # Always 3 upper case letters
    CSV_COLUMN(1, 'tracksite', None),

    # The level within the track site specifying the excavation depth where
    # the track resided. Lower numbers are deeper in the excavation and are
    # therefore older.
    CSV_COLUMN(2, 'level', None),

    # Represents the trackway type, e.g. S for Sauropod, and the trackway
    # number within the tracksite and level. Suffices can include 'bis' for a
    # trackway that was broken but could be a continuation of the previous
    # version.
    CSV_COLUMN(3, 'trackway', None),

    # The excavation area within the tracksite where the track was found
    CSV_COLUMN(4, 'sector', None),

    # CATALOG ONLY: Entry angle for the trackway as measured by the
    # Illustrator file.
    CSV_COLUMN(5, 'entry_azimuth', ''),

    # CATALOG ONLY: Exit angle for the trackway as measured by the Illustrator
    # file.
    CSV_COLUMN(6, 'exit_azimuth', ''),

    # CATALOG ONLY: Information that specifies the total orientation
    CSV_COLUMN(7, 'direct_azimuth', ''),

    # CATALOG ONLY: Trackway length as measured by the illustrator file.
    CSV_COLUMN(8, 'trackway_length', None),

    # CATALOG ONLY: Illustrator file measurement.
    CSV_COLUMN(9, 'comment', ''),

    # CATALOG ONLY: Illustrator file measurement.
    CSV_COLUMN(10, 'azimuth_deviation', ''),

    # CATALOG ONLY: Illustrator file measurement.
    CSV_COLUMN(11, 'azimuth_mean', ''),

    # CATALOG ONLY: Illustrator file measurement.
    CSV_COLUMN(12, 'azimuth_mean_deviation', ''),

    # CATALOG ONLY: Categorical reference for track types, such as straight,
    # curved, etc.
    CSV_COLUMN(13, 'orientations', ''),

    # Reference material exists for a plastic sheet drawing at 1:1 for the
    # track.
    CSV_COLUMN(14, 'outline_drawing', ''),

    # Reference material of the original print exists in the collection.
    CSV_COLUMN(15, 'preserved', ''),

    # Reference material exist as a cast in the collection.
    CSV_COLUMN(16, 'cast', ''),

    # Initials of the person or people who took the data.
    CSV_COLUMN(17, 'measured_by', 'KS'),

    # The date when the print was measured in the field.
    CSV_COLUMN(18, 'measured_date', ''),

    # Name of person in the office that took the measured data and entered.
    CSV_COLUMN(19, 'data_entered_by', 'SE'),

    # The date the measured data was entered in the computer.
    CSV_COLUMN(20, 'data_entry_date', '12/1/2016'),

    # The name of the track within the trackway.
    CSV_COLUMN(21, 'track_name', None),

    # A fictional possible track to explain missing.
    CSV_COLUMN(22, 'missing', ''),

    # Fundamental track measurements made in the field
    CSV_COLUMN(23, 'pes_length', None),
    CSV_COLUMN(24, 'pes_length_guess', None),
    CSV_COLUMN(25, 'pes_width', None),
    CSV_COLUMN(26, 'pes_width_guess', None),
    CSV_COLUMN(27, 'pes_depth', ''),
    CSV_COLUMN(28, 'pes_depth_guess', ''),
    CSV_COLUMN(33, 'manus_length', None),
    CSV_COLUMN(34, 'manus_length_guess', None),
    CSV_COLUMN(35, 'manus_width', None),
    CSV_COLUMN(36, 'manus_width_guess', None),
    CSV_COLUMN(37, 'manus_depth', ''),
    CSV_COLUMN(38, 'manus_depth_guess', ''),

    # Rotation (in degrees) measured locally using center-to-center track
    # segments as the 0 line. Positive values indicate outward rotation and
    # negative values inward relative the body.
    CSV_COLUMN(29, 'left_pes_rotation', None),
    CSV_COLUMN(30, 'left_pes_rotation_guess', None),
    CSV_COLUMN(31, 'right_pes_rotation', None),
    CSV_COLUMN(32, 'right_pes_rotation_guess', None),
    CSV_COLUMN(39, 'left_manus_rotation', None),
    CSV_COLUMN(40, 'left_manus_rotation_guess', None),
    CSV_COLUMN(41, 'right_manus_rotation', None),
    CSV_COLUMN(42, 'right_manus_rotation_guess', None),

    # Center-to-center measurement between successive prints. If a track or
    # more were missing the measurement was made to the next available track
    # and then divided by the interpretation of the number of missing tracks
    # as defined by the stride factor.
    CSV_COLUMN(43, 'pes_stride', None),
    CSV_COLUMN(44, 'pes_stride_guess', None),
    CSV_COLUMN(45, 'pes_stride_factor', None),
    CSV_COLUMN(58, 'manus_stride', None),
    CSV_COLUMN(59, 'manus_stride_guess', None),
    CSV_COLUMN(60, 'manus_stride_factor', None),

    # WAP & WAM as measured in the field according to Daniel's thesis in
    # Figure 2.11.
    CSV_COLUMN(46, 'width_pes_angulation_pattern', ''),
    CSV_COLUMN(47, 'width_pes_angulation_pattern_guess', ''),
    CSV_COLUMN(61, 'width_manus_angulation_pattern', ''),
    CSV_COLUMN(62, 'width_manus_angulation_pattern_guess', ''),

    # Diagonal distance between the track and the corresponding next track on
    # the opposite side of the body/trackway.
    CSV_COLUMN(48, 'left_pes_pace', None),
    CSV_COLUMN(49, 'left_pes_pace_guess', None),
    CSV_COLUMN(52, 'right_pes_pace', None),
    CSV_COLUMN(53, 'right_pes_pace_guess', None),
    CSV_COLUMN(63, 'left_manus_pace', None),
    CSV_COLUMN(64, 'left_manus_pace_guess', None),
    CSV_COLUMN(67, 'right_manus_pace', None),
    CSV_COLUMN(68, 'right_manus_pace_guess', None),

    # Angle in degrees of successive pace measurements between tracks.
    CSV_COLUMN(56, 'pes_pace_angulation', ''),
    CSV_COLUMN(57, 'pes_pace_angulation_guess', ''),
    CSV_COLUMN(71, 'manus_pace_angulation', ''),
    CSV_COLUMN(72, 'manus_pace_angulation_guess', ''),

    # A calculated measurement
    CSV_COLUMN(50, 'left_pes_progression', ''),
    CSV_COLUMN(51, 'left_pes_progression_guess', ''),
    CSV_COLUMN(54, 'right_pes_progression', ''),
    CSV_COLUMN(55, 'right_pes_progression_guess', ''),
    CSV_COLUMN(65, 'left_manus_progression', ''),
    CSV_COLUMN(66, 'left_manus_progression_guess', ''),
    CSV_COLUMN(69, 'right_manus_progression', ''),
    CSV_COLUMN(70, 'right_manus_progression_guess', ''),

    # Measurement as described in Daniel's thesis in figure 2.13.
    CSV_COLUMN(73, 'gleno_acetabular_distance', ''),
    CSV_COLUMN(74, 'gleno_acetabular_distance_guess', ''),

    # CATALOG ONLY: Comments about toe, claw, etc. impressions in the print.
    CSV_COLUMN(75, 'anatomical_details', '')
]

cd.shared.csv_columns = sorted(csv_columns, key=lambda col: col[0])
