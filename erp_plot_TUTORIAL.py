# Authors: Martin Billinger <martin.billinger@tugraz.at>

# License: BSD (3-clause)

import mne
import numpy as np
from mne import Epochs, pick_types, find_events, channels
from mne.io import concatenate_raws, read_raw_edf
from mne.time_frequency import tfr_morlet


class erp_plot:
    def __init__(self):
        pass

    def plotERP(self, event_code1=769, event_code2=770, filename="",
                bad_ch=['Channel 14', "Channel 15", "EMG1", "Channel 17", "Channel 18", "Channel 19", "T10"], ):
        tmin, tmax = -1., 4.
        event_id = dict(class1=event_code1, class2=event_code2)

        # load file
        raw_fnames = [filename]
        raw_files = [read_raw_edf(f, preload=True, stim_channel='auto') for f in
                     raw_fnames]
        raw = concatenate_raws(raw_files)
        montage = channels.read_montage('standard_1020')
        raw.set_montage(montage)

        raw.info['bads'] = bad_ch
        events = find_events(raw, shortest_event=0)

        # select what to print and what to exclude
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                           exclude='bads')

        reject = dict(eeg=180e-6)

        evoked_no_ref = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                               baseline=(-0.5, 0), reject=reject, preload=True).average()

        title = 'EEG'
        evoked_no_ref.plot(titles=dict(eeg=title), time_unit='s', spatial_colors=True)

        # define frequencies of interest (log-spaced)
        freqs = np.logspace(*np.log10([6, 35]), num=8)
        n_cycles = freqs / 2.  # different number of cycle per frequency
        power, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                                return_itc=True, decim=3, n_jobs=1)

        power.plot_joint(baseline=(-0.5, 0), mode='logratio', tmin=tmin, tmax=tmax,
                         timefreqs=[(.5, 10), (1.3, 8)])


# #############################################################################
# # Set parameters and read data

# avoid classification of evoked responses by using epochs that start 1s after
# cue onset.
tmin, tmax = -1., 4.
event_id = dict(class1=770, class2=769)
# event_id = dict(hands=2, feet=3)

subject = 1
runs = [6, 10, 14]  # motor imagery: hands vs feet

# raw_fnames = ['C:/Users/aleks/Desktop/MyExperiment/1/1/training_data.gdf']
raw_fnames = ['/private/tmp/training_data23.gdf']
# raw_fnames = ['/Users/aleksandarmiladinovic/mne_data/MNE-eegbci-data/physiobank/database/eegmmidb/S001/S001R14.edf']

raw_files = [read_raw_edf(f, preload=True, stim_channel='auto') for f in
             raw_fnames]
raw = concatenate_raws(raw_files)

# strip channel names of "." characters
raw.rename_channels(lambda x: x.strip('.'))

# Apply band-pass filter
raw.filter(1., 45., fir_design='firwin', skip_by_annotation='edge')
raw.info['bads'] = ['Channel 14', "Channel 15", "EMG1", "Channel 17", "Channel 18", "Channel 19", "T10"]
raw.info['bads'] = ['EMG']

montage = channels.read_montage('standard_1020')

raw.set_montage(montage)
raw.plot(block=True, lowpass=40)
# raw.plot_sensors()




print "HHHHH"
print raw.info['bads']
print "HHHHH"

events = find_events(raw, shortest_event=0)

picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                   exclude='bads')

# picks = pick_channels(raw.info["ch_names"], ["C3", "C4"])

reject = dict(eeg=180e-6)

evoked_no_ref = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                       baseline=None, reject=reject, preload=True).average()
epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                baseline=(-0.5, 0), reject=reject, preload=True)
edi = {'Class1 (left)': epochs["class1"].average(), 'Class2 (Right)': epochs["class2"].average()}
fig = mne.viz.plot_compare_evokeds(edi, gfp=True)

title = 'EEG Original reference'
evoked_no_ref.plot(titles=dict(eeg=title), time_unit='s', spatial_colors=True)
# evoked_no_ref.plot_topomap(times=[0.1], size=3., title=title, time_unit='s')


evoked_no_ref.plot(titles=dict(eeg=title), time_unit='s', spatial_colors=True)

epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                baseline=(-0.5, 0), reject=reject, preload=True)
print "1"
epochs["class1"].plot_psd(fmin=2., fmax=40.)
epochs["class2"].plot_psd(fmin=2., fmax=40.)

print "2"
epochs["hand"].plot_image(combine='gfp', group_by='type', sigma=2., cmap='interactive')
epochs.plot_psd_topomap(normalize=True)
epochs.plot_image(picks=picks)
epochs.plot_psd_topomap()
epochs.plot_topo_image()

# define frequencies of interest (log-spaced)
freqs = np.logspace(*np.log10([6, 35]), num=8)
n_cycles = freqs / 2.  # different number of cycle per frequency
power, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)

power.plot_joint(baseline=(-0.5, 0), mode='logratio', tmin=tmin, tmax=tmax,
                 timefreqs=[(.5, 10), (1.3, 8)])
# power.plot(baseline=(-0.5, 0), tmin=tmin, tmax=tmax, mode='logratio')
