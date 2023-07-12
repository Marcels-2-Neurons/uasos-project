# JUST FOR DEBUG PURPOSES

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # It's just a second instance to run into a separate console instance

    from pylsl import StreamInlet, resolve_stream

    # first resolve a marker stream on the lab network
    print("looking for a marker stream...")
    streams = resolve_stream('type', 'Markers')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    close = False

    while not close:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        print("%s : %s" % (timestamp, sample))
        if sample[0] == 'CLS-0000-000-0-0':
            close = True
