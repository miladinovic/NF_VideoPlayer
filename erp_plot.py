import mne
import numpy as np
from mne import Epochs, pick_types, find_events, channels
from mne.io import concatenate_raws, read_raw_edf
from mne.time_frequency import tfr_morlet


class erp_plot:
    def __init__(self):
        pass

    def plotERP(self, event_code1=769, event_code2=770, filename="", bad_ch=["EMG"]):



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

        # Apply band-pass filter
        raw.filter(1., 45., fir_design='firwin', skip_by_annotation='edge')

        # plot channels
        # raw.plot(block=True, lowpass=40,title="EEG Traces : Click on channels to exclude them!")



        #select what to print and what to exclude
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                           exclude='bads')

        baseline_correction = (-0.5, 0)
        epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                        baseline=baseline_correction, preload=True)
        epochsAVGclass1 = epochs["class1"].average()
        epochsAVGclass2 = epochs["class2"].average()

        title = 'EEG - Class 1 (left)'
        # epochsAVGclass1.plot(titles=dict(eeg=title), time_unit='s', spatial_colors=True, gfp=True)
        title = 'EEG - Class 2 (right)'
        # epochsAVGclass2.plot(titles=dict(eeg=title), time_unit='s', spatial_colors=True,gfp=True)

        edi = {'Class1 (left)': epochs["class1"].average(), 'Class2 (Right)': epochs["class2"].average()}
        fig = mne.viz.plot_compare_evokeds(edi, gfp=True)
        print fig

        # define frequencies of interest (log-spaced)
        freqs = np.logspace(*np.log10([6, 35]), num=8)
        n_cycles = freqs / 2.  # different number of cycle per frequency
        power, itc = tfr_morlet(epochs["class1"], freqs=freqs, n_cycles=n_cycles, use_fft=True, return_itc=True,
                                decim=3, n_jobs=1)

        # power.plot_joint(title="Class 1 - left",baseline=(-0.5, 0), mode='logratio', tmin=tmin, tmax=tmax,timefreqs=[(.5, 10), (1.3, 8)])

        power, itc = tfr_morlet(epochs["class2"], freqs=freqs, n_cycles=n_cycles, use_fft=True, return_itc=True,
                                decim=3, n_jobs=1)

        # power.plot_joint(title="Class2 - right",baseline=(-0.5, 0), mode='logratio', tmin=tmin, tmax=tmax,timefreqs=[(.5, 10), (1.3, 8)])

        # epochs["class1"].plot_psd(fmin=2., fmax=40.)
        # epochs["class2"].plot_psd(fmin=2., fmax=40.)

        # epochs["class1"].plot_image(title="Plot_image: Class1 - (left)",combine='gfp', group_by='type', sigma=2., cmap='interactive')
        # epochs["class2"].plot_image(title="Plot_image: Class2 - (right)",combine='gfp', group_by='type', sigma=2., cmap='interactive')
        print "bye"


if __name__ == "__main__":
    import matplotlib

    ploter = erp_plot()
    # ploter.plotERP(filename="/private/tmp/training_data.gdf")
    ploter.plotERP(filename="C:/Users/aleks/Desktop/MyExperiment/1/1/training_data.gdf")
