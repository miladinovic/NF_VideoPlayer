# Authors: Martin Billinger <martin.billinger@tugraz.at>

# License: BSD (3-clause)

import numpy as np
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import ShuffleSplit, cross_val_score

from mne import Epochs, pick_types, find_events, channels, pick_channels
from mne.channels import read_layout
from mne.io import concatenate_raws, read_raw_edf, find_edf_events
from mne.datasets import eegbci
from mne.decoding import CSP
from mne.time_frequency import tfr_morlet, psd_multitaper
from mne.time_frequency import tfr_multitaper
import mne
from mne.time_frequency import tfr_morlet, psd_multitaper
from mne.datasets import somato
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import mne
from mne.datasets import eegbci
from mne.io import concatenate_raws, read_raw_edf
from mne.time_frequency import tfr_multitaper
from mne.stats import permutation_cluster_1samp_test as pcluster_test


class erp_plot:
    def __init__(self):
        pass

    def plot(self, event_code=770, filename="", bad_ch=[]):
        tmin, tmax = -1., 4.
        event_id = dict(hand=event_code)
        raw_fnames = [filename]
        raw_files = [read_raw_edf(f, preload=True, stim_channel='auto') for f in
                     raw_fnames]
        raw = concatenate_raws(raw_files)
        montage = channels.read_montage('standard_1020')
        raw.set_montage(montage)

        raw.info['bads'] = bad_ch
        events = find_events(raw, shortest_event=0)

        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                           exclude='bads')

        reject = dict(eeg=180e-6)

        evoked_no_ref = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                               baseline=None, reject=reject, preload=True).average()

        title = 'EEG'
        evoked_no_ref.plot(titles=dict(eeg=title), time_unit='s', spatial_colors=True)


# #############################################################################
# # Set parameters and read data

# avoid classification of evoked responses by using epochs that start 1s after
# cue onset.
tmin, tmax = -1., 4.
event_id = dict(hand=770, hand2=769)
# event_id = dict(hands=2, feet=3)

subject = 1
runs = [6, 10, 14]  # motor imagery: hands vs feet

# raw_fnames = ['C:/Users/aleks/Desktop/MyExperiment/1/1/training_data.gdf']
raw_fnames = ['/private/tmp/training_data.gdf']
# raw_fnames = ['/Users/aleksandarmiladinovic/mne_data/MNE-eegbci-data/physiobank/database/eegmmidb/S001/S001R14.edf']

raw_files = [read_raw_edf(f, preload=True, stim_channel='auto') for f in
             raw_fnames]
raw = concatenate_raws(raw_files)

# strip channel names of "." characters
raw.rename_channels(lambda x: x.strip('.'))

# Apply band-pass filter
raw.filter(1., 45., fir_design='firwin', skip_by_annotation='edge')
raw.info['bads'] = ['Channel 14', "Channel 15", "EMG1", "Channel 17", "Channel 18", "Channel 19", "T10"]

montage = channels.read_montage('standard_1020')

raw.set_montage(montage)
raw.plot(block=True, lowpass=40)
# raw.plot_sensors()


events = find_events(raw, shortest_event=0)

picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                   exclude='bads')

picks = pick_channels(raw.info["ch_names"], ["C3", "C4"])

reject = dict(eeg=180e-6)

evoked_no_ref = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                       baseline=None, reject=reject, preload=True).average()

title = 'EEG Original reference'
evoked_no_ref.plot(titles=dict(eeg=title), time_unit='s', spatial_colors=True)
# evoked_no_ref.plot_topomap(times=[0.1], size=3., title=title, time_unit='s')



epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                baseline=None, reject=reject, preload=True)
print epochs
epochs.plot_psd(fmin=2., fmax=40.)
epochs.plot_psd_topomap(normalize=True)

# define frequencies of interest (log-spaced)
freqs = np.logspace(*np.log10([6, 35]), num=8)
n_cycles = freqs / 2.  # different number of cycle per frequency
power, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)

power.plot_joint(baseline=(-0.5, 0), mode='mean', tmin=-.5, tmax=2,
                 timefreqs=[(.5, 10), (1.3, 8)])
