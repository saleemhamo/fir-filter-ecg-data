# ENG5027- DIGITAL SIGNAL PROCESSING
## Assignment 2: FIR Filters

## Introduction
This project will analyze ECG signals using FIR filters; initially, the ECG signal (ECG_1000Hz_14.dat) was read using Python. To create a clean ECG signal, a generic FIR filter was first designed. Then, frequency and impulse response for high-pass and band stop filters were computed and applied using the FIR filter logic to eliminate the DC component from the ECG signal as well as the 50Hz signal (noise).
The clean signal will then be subjected to a matching filter to identify heartbeats. Two approaches were followed: one involved extracting a wavelet from the signal directly, and the other involved using a (Sinc) pulse.
Another filtration step was performed using the LMS filter, which included generating a 50Hz reference signal and applying an adaptive LMF filter to clean the original one.

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/6cd8405e-de0e-4879-8778-c5f2cdab15f6)

![image](https://github.com/saleemhamo/fir-filter-ecg-data/assets/55649338/5a88c364-23d0-4852-847a-652d0c4ba6ce)


...

## Task 1: Calculate FIR Coefficients
### Band-stop filter design
...

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
