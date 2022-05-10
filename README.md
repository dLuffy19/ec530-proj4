# EC530 Project 4

## Phase 1: Queueing System

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