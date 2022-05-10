# Speech to text module

import deepspeech
import wave
import numpy as np

# Setup model
def setup_model():
    model_path = 'deepspeech-0.6.0-models/output_graph.pbmm'
    beam_width = 500
    model = deepspeech.Model(model_path, beam_width)
    language_model_path = 'deepspeech-0.6.0-models/lm.binary'
    trie_file_path = 'deepspeech-0.6.0-models/trie'
    language_model_alpha = 0.75
    language_model_beta = 1.85
    model.enableDecoderWithLM(language_model_path, trie_file_path, language_model_alpha, language_model_beta)
    return model

# Call batch API
def call_batch(filename, model):
    w = wave.open(filename, 'r')
    rate = w.getframerate()
    frames = w.getnframes()
    buffer = w.readframes(frames)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    text = model.stt(data16)
    print(text)

# Call streaming API
def call_stream(filename, model):
    w = wave.open(filename, 'r')
    frames = w.getnframes()
    buffer = w.readframes(frames)
    context = model.createStream()
    buffer_len = len(buffer)
    offset = 0
    batch_size = 16384
    text = ''
    while offset < buffer_len:
        end_offset = offset + batch_size
        chunk = buffer[offset:end_offset]
        data16 = np.frombuffer(chunk, dtype=np.int16)
        model.feedAudioContent(context, data16)
        text = model.intermediateDecode(context)
        print(text)
        offset = end_offset
    text = model.finishStream(context)
    print(text)

if __name__ == '__main__':
    model = setup_model()
    print('Calling batch API...')
    call_batch('audio/8455-210777-0068.wav', model)
    print('Calling streaming API...')
    call_stream('audio/8455-210777-0068.wav', model)