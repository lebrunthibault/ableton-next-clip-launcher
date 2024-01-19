import Live


# allows firing the clip at the quantization limit so it's clearer when it is fired
quantization_to_bars = {
    Live.Song.Quantization.q_8_bars: 8,
    Live.Song.Quantization.q_4_bars: 4,
    Live.Song.Quantization.q_2_bars: 2,
    Live.Song.Quantization.q_bar: 1,
    Live.Song.Quantization.q_half: 1.0 / 2,
    Live.Song.Quantization.q_half_triplet: 1.0 / 3,
    Live.Song.Quantization.q_quarter: 1.0 / 4,
    Live.Song.Quantization.q_quarter_triplet: 1.0 / 6,
    Live.Song.Quantization.q_eight: 1.0 / 8,
    Live.Song.Quantization.q_eight_triplet: 1.0 / 12,
    Live.Song.Quantization.q_sixtenth: 1.0 / 16,
    Live.Song.Quantization.q_sixtenth_triplet: 1.0 / 24,
    Live.Song.Quantization.q_thirtytwoth: 1.0 / 32,
}

def _get_track_clips(track):
    # type: (Live.Track.Track) -> list
    clips = []
    for cs in track.clip_slots:
        if cs.clip:
            clips.append(cs.clip)

    return clips

def get_playing_clip(track):
    for clip in _get_track_clips(track):
        if clip.is_playing:
            return clip

    return None

def get_next_clip(track):
    clips = _get_track_clips(track)
    for index, clip in enumerate(clips):
        if clip.is_playing:
            try:
                return clips[index + 1]
            except IndexError:
                return None

def can_clip_be_fired(clip, clip_trigger_quantization, signature_numerator, signature_denominator):
    # type: (Live.Clip.Clip, Live.Song.Quantization, int, int) -> bool
    quantization_bars = quantization_to_bars[clip_trigger_quantization]
    quantization_beats = quantization_bars * (float(signature_numerator) / signature_denominator)

    clip_beat_lefts = clip.length - clip.playing_position
    # logging.info("quantization : %s beats, beats left: %.2f" % (quantization_beats, clip_beat_lefts))

    return clip_beat_lefts < quantization_beats
