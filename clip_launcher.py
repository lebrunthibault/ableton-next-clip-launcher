import logging

from _Framework.ButtonElement import ButtonElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_NOTE_TYPE
from _Framework.SubjectSlot import subject_slot
from playing_clip import get_next_clip, can_clip_be_fired, get_playing_clip


class ClipLauncher(ControlSurface):
    def __init__(self, c_instance):
        super(ClipLauncher, self).__init__(c_instance=c_instance)

        logging.info(
            "ClipLauncher started, clip trigger quantization: %s"
            % self.song().clip_trigger_quantization
        )

        with self._component_guard():
            # Listen on midi channel 2 (indexes start at 0) for midi note 0 (C-2)
            self._press_listener.subject = ButtonElement(True, MIDI_NOTE_TYPE, 1, 0)

        self._current_song_time_listener.subject = self.song()
        self._playing_clip = None
        self._launch_next_clip = False

    @property
    def selected_track(self):
        """Access the selected track"""
        return self.song().view.selected_track

    def reset_launch(self):
        """Reset the Clip Launcher state"""
        self._playing_clip = None
        self._launch_next_clip = False

    @subject_slot("value")
    def _press_listener(self, value):
        """Reacts to the button push by scheduling the next clip launch"""
        if not value:
            return

        if not self.song().is_playing:
            self.reset_launch()
            logging.info("Song is not playing")
            return

        self._playing_clip = get_playing_clip(self.selected_track)
        if not self._playing_clip:
            self.reset_launch()
            logging.info("No playing clip")
            return

        if not get_next_clip(self.selected_track):
            self.reset_launch()
            logging.info("No Clip to launch")
            return

        self._launch_next_clip = True
        logging.info("Clip launcher scheduled, after '%s'" % self._playing_clip.name)

    @subject_slot("current_song_time")
    def _current_song_time_listener(self):
        """
        Checks periodically that the next clip should be launched
        depending on the global clip trigger quantization value and the time signature
        """
        if not self._launch_next_clip:  # no clip scheduled for launch
            return

        if self._playing_clip != get_playing_clip(self.selected_track):
            self.reset_launch()
            logging.info("Playing clip mismatch, launch cancelled")
            return

        next_clip = get_next_clip(self.selected_track)
        if not next_clip:
            self.reset_launch()
            logging.info("No Clip to launch")
            return

        if can_clip_be_fired(
            self._playing_clip,
            self.song().clip_trigger_quantization,
            self.song().signature_numerator,
            self.song().signature_denominator,
        ):
            logging.info("Firing clip '%s'" % next_clip.name)

            next_clip.fire()
            self.reset_launch()

    def _on_selected_track_changed(self):
        """Hide detail panel when selected track is changed"""
        self.application().view.hide_view("Detail")
