# ENG5027- DIGITAL SIGNAL PROCESSING
## Assignment 2: FIR Filters

## Introduction
This project will analyze ECG signals using FIR filters; initially, the ECG signal (ECG_1000Hz_14.dat) was read using Python. To create a clean ECG signal, a generic FIR filter was first designed. Then, frequency and impulse response for high-pass and band stop filters were computed and applied using the FIR filter logic to eliminate the DC component from the ECG signal as well as the 50Hz signal (noise).
The clean signal will then be subjected to a matching filter to identify heartbeats. Two approaches were followed: one involved extracting a wavelet from the signal directly, and the other involved using a (Sinc) pulse.
Another filtration step was performed using the LMS filter, which included generating a 50Hz reference signal and applying an adaptive LMF filter to clean the original one.

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/6cd8405e-de0e-4879-8778-c5f2cdab15f6)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/5a88c364-23d0-4852-847a-652d0c4ba6ce)


## Task 1: Calculate FIR Coefficients
In this part, the goal is to build the FIR filter coefficients that will be used in designing the FIR Filter. First, the frequency responses will be calculated, then applied to the ifft function, resulting the impulse repose. After that, the impulse response will be shifted to the time domain (swapped).

### Band-stop filter design
![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/259ad67e-1907-4b75-a8e2-f5dcd8cb6a61)

The first step was creating the frequency response using python arrays. As the figure below shows:

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/f7d64ac7-b543-4a0b-b03e-b9f7d8f75edf)

After that, the ifft of the frequency response was calculated, to obtain the impulse response.

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/ded52c84-24f3-4d9e-b6b5-b5eaf730a5b3)

Shifting (swapping) to the positive time was performed on the resulted impulse response.

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/04e9fade-3aef-4c1a-9755-a3bbd17987c7)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/d063341f-afad-44fa-a23e-21396990a053)


### High pass filter design

The same steps from the previous section apply here.
![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/01611f1e-2f93-4264-8660-580278d4a74c)
![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/4b725fd8-f034-4da3-89d4-df975a0aae6a)
![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/037760d1-edcd-4dc4-8e4a-dda544ae034a)
![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/0ba2bdea-c397-4f0d-ae2e-f185268884b3)



## Task 2: 50Hz Removal Using High-pass Filter

This task's target is to remove 50 Hz interference and the baseline wander with high-pass filter and band-stop filter designed in task 1. And with the Finite Impulse Response filter implemented and cutoff frequency decided, the approach used was as follows:

### Design of FIR dofilter
The FIR filter processes signal by discretely convolving the input signal in time domain. A crucial property of convolution is that the convolution in the time domain is equivalent to multiplication in the frequency domain, which is intimately connected to filtering because the purpose of filtering is to obtain specific frequency components. Frequency domain multiplication is precisely the operation that achieves this filtering objective.
As both the value argument and return value of dofilter are scalars and not vectors, we cannot use arrays to perform convolution operations because arrays are not iterable. Compared with arrays, lists are iterable and mutable, allowing dynamic addition, deletion, and modification of elements. Therefore, a buffer is used to store the input values as a shift register. By adding the product of each pair of value and coefficient, we achieve the convolution operation of the filter.

Selecting cutoff frequency
Band-stop: 45-55 Hz

The figure of original ECG signal shows that there is a 50Hz interference in frequency domain which typically arises from the influence of alternating current signals from the power system. As the amplitudes of frequencies around 50Hz are low, we decide 45-55 Hz as the band-stop filter cutoff.
After doing band-stop filter, the results are as shown in the following graphs

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/66e80cd0-6ec0-495a-bb5d-2780dfd0e49e)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/000905e7-9855-4230-9181-ce4c6911468b)


·High-pass: 0.5 Hz
The following graph depicts the frequency-domain representation of an ECG signal. To better visualize the frequency of baseline drift, we set the horizontal axis to a logarithmic scale. And it is evident that there is significant low-frequency noise present before 0.5Hz.

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/fc801039-c86c-4cf1-86fa-dd428606263c)

Considering the aforementioned factors, we choose 0.5Hz as the cutoff frequency for the high-pass filter, the signal filtered by the high-pass filter is as shown in the following graphs, It’s clear that the clean signal has a delay in time, which is expected to have because of the used buffer size of the FIR filter.

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/0c1bd2e8-2594-40a6-8298-8d94a062dafc)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/28037c95-bdfd-4c9b-b631-0dfea818f428)



## Task 3: 50Hz Removal using Adaptive LMS Filter
In this section, the adaptive interference removal is explored using the Least Mean Square (LMS) algorithm as a replacement for the bandstop filter used in FIR filter. However, the same highpass filter from the FIR filter will still be used to eliminate the DC component.

To begin with, unlike the FIR filter, the LMS filter actively adjusts the coefficients based on the real-time difference between the ECG signal development and the 50Hz reference noise. The goal of this filter is to eliminate the noise and to preserve the ECG signal. Hence, the implementation of the LMS filter was as follows:

Some functions from FIR filter code such as the constructor of the class and some methods such as the doFilter were preserved however, there were minor additions such as the introduction of the coefficients and taps.
Additionally, the adaptive filtering loop (do_filter_adaptive) was applied to dynamically tune the coefficients based on the error obtained from the difference between the raw ECG data and the reference noise.
Moreover, in the processing loop (filter_signal_lms), each sample from the original ECG signal is processed individually. And for each iteration, a reference noise signal is generated as a sine wave with a frequency 50Hz (f_noise). The sine wave is then combined with the current ECG sample using the adaptive LMS filter providing a clean ECG signal without the 50Hz noise as an output.
Also, the attempted values for the learning rate in the (filter_signal_lms) processing loop were 0.1, 0.01 and 0.001, and with the 0.1 learning rate did not produce a meaningful ECG signal, and with the 0.001, the processing time was too long while it gave the same graph as the one with the 0.01 learning rate, hence the choice of the learning rate was made for it to be 0.01.
The output is then stored into the (filtered_signal) array, and the process is repeated for every sample of the ECG signal. Lastly, the data obtained from the (filtered_signal) array is then used for the plotting of the cleaned-up ECG signal graph.
It is crucial to note that, unlike theory suggests, the 50Hz signal was utilized as the reference signal instead of the cleaned-up ECG signal obtained from the FIR filter for the comparative analysis between the performance of the FIR filter and the LMS filter, and the fact that both filters were being worked on simultaneously. The cleaned-up ECG signal obtained from the LMS filter was as shown below:

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/3e18e087-ef68-416b-9935-be6d994f504c)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/eb9cb3b3-b437-4a4f-b93e-3592caf12bc4)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/cce2e8ba-4174-4baa-8919-ee75a5a80534)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/5bc37a12-fba3-4d4b-9001-fb560f09c883)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/8c28e6bf-0d8b-4a1f-b3c8-1f4790a76a0f)



## Task 4: ECG Heartbeat detection using Matched Filter

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/b825dd42-89d3-4296-b4cf-1ac9f537c80c)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/b11de8be-ef9e-4cab-9cdc-9eba9662b237)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/f00d016f-11b5-49e8-b174-a4748a41c8a1)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/132f72cc-4060-4f38-96d7-79e8b06c5415)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/8ada3259-6492-4acd-b916-3c6c7ad31671)



