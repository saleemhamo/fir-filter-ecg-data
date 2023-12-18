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
...

## Task 2: 50Hz Removal Using High-pass Filter
...

## Task 3: 50Hz Removal using Adaptive LMS Filter
...

## Task 4: ECG Heartbeat detection using Matched Filter
...

## Appendix
### Python Code
- [firfilter.py](#firfilterpy)
- [filterdesign.py](#filterdesignpy)
- [hpbsfilter.py](#hpbsfilterpy)
- [hrdetect.py](#hrdetectpy)
- [lmsfilter.py](#lmsfilterpy)
- [helper.py](#helperpy)
