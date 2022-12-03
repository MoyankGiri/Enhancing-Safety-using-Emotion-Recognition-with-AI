from flask import Flask, render_template, Response, request, url_for, redirect
from camera import Video
import pyaudio

app = Flask(__name__, static_url_path='/static')

#audio1 = pyaudio.PyAudio()
p = pyaudio.PyAudio()

def generate_wav(self, raw):
	"""
	Create WAVE-file from raw audio chunks
	@param bytes raw
	@return bytes
	"""
	# Check if input format is supported
	if self.FORMAT not in (pyaudio.paFloat32, pyaudio.paInt16):
		print("Unsupported format")
		return
	# Convert raw audio bytes to typed array
	samples = self.bytes_to_array(raw, np.float32)
	# Get sample size
	sample_size = pyaudio.get_sample_size(self.FORMAT)
	# Get data-length
	byte_count = (len(samples)) * sample_size
	# Get bits/sample
	bits_per_sample = sample_size * 8
	# Calculate frame-size
	frame_size = int(self.CHANNELS * ((bits_per_sample + 7) / 8))
	# Container for WAVE-content
	wav = bytearray()
	# Start RIFF-Header
	wav.extend(struct.pack('<cccc', b'R', b'I', b'F', b'F'))
	# Add chunk size (data-size minus 8)
	wav.extend(struct.pack('<I', byte_count + 0x2c - 8))
	# Add RIFF-type ("WAVE")
	wav.extend(struct.pack('<cccc', b'W', b'A', b'V', b'E'))
	# Start "Format"-part
	wav.extend(struct.pack('<cccc', b'f', b'm', b't', b' '))
	# Add header length (16 bytes)
	wav.extend(struct.pack('<I', 0x10))
	# Add format-tag (e.g. 1 = PCM, 3 = FLOAT)
	wav.extend(struct.pack('<H', 3))
	# Add channel count
	wav.extend(struct.pack('<H', self.CHANNELS))
	# Add sample rate
	wav.extend(struct.pack('<I', self.RATE))
	# Add bytes/second
	wav.extend(struct.pack('<I', self.RATE * frame_size))
	# Add frame size
	wav.extend(struct.pack('<H', frame_size))
	# Add bits/sample
	wav.extend(struct.pack('<H', bits_per_sample))
	# Start data-part
	wav.extend(struct.pack('<cccc', b'd', b'a', b't', b'a'))
	# Add data-length
	wav.extend(struct.pack('<I', byte_count))
	# Add data
	for sample in samples:
		wav.extend(struct.pack("<f", sample))
	return bytes(wav)

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

def generateAudio():
        FORMAT = pyaudio.paInt16 
        CHUNK = 262144 
        CHANNELS = 2
        RATE = 44100 #48000
        RECORD_SECONDS = 10
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        #p = pyaudio.PyAudio()
        wav_header = genHeader(sampleRate, bitsPerSample, channels)
        stream = p.open(format=FORMAT,
                	channels=CHANNELS,
                	rate=RATE,
                	input=True,
					input_device_index=1,
                	output=True,
                	frames_per_buffer=CHUNK)

        print("done")

        while True:
            data = wav_header+stream.read(CHUNK)
            yield(data)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/audio")
def audio():
    return Response(generateAudio(), mimetype="audio/x-wav;codec=pcm")

if __name__ == "__main__":  # new
    app.run(host='0.0.0.0', debug=True, threaded=True,port=5000)
