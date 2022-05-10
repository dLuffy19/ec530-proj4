# EC530 Project 4

## Phase 1: Queueing System

### Scenario

This is a M/M/2 queueing system:
My system has two servers, which means there're at most 2 stub functions running at the same time, the remaining functions should be waiting in queue. The running time of each stub function depends on server capability (I set 1.5 minutes for server 1, and 1.7 minutes for server 2). Every 2 minutes there's a new stub function coming in.

The Python script will show the statistic info of  the result after 240 minutes (not real world time).

### Setup

You'll need two packages to run the module:
* numpy
* pandas

```shell
pip install numpy
pip install pandas
```

## Phase 2: Speech to Text Module

For speech to text module, I used [Mozilla DeepSpeech API](https://github.com/mozilla/DeepSpeech).

### Setup

Create and activate Python virtual environment
```shell
python3 -m venv stt
source stt/bin/activate
```

Install DeepSpeech
```shell
python3 -m pip install deepspeech==0.6.0
```

Download and unzip models
```shell
mkdir ds
cd ds
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.0/deepspeech-0.6.0-models.tar.gz
tar -xvzf deepspeech-0.6.0-models.tar.gz
```

Download some audio samples (make sure you are inside `ds` folder)
```shell
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.0/audio-0.6.0.tar.gz
tar -xvzf audio-0.6.0.tar.gz
```

Test API
```shell
python3 speech_to_text.py
```