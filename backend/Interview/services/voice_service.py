"""
Voice Service
Responsible for processing interview audio.
Responsibilities:
- Validate uploaded audio
- Temporarily store audio
- Convert speech to text
- Calculate basic voice metadata
This service contains no interview business logic.
"""

import os
import tempfile
from faster_whisper import WhisperModel

class VoiceService:

    def __init__(self):

        self.model = None

    def _get_model(self):
        if self.model is None:
            self.model = WhisperModel(
                "base",
                device="cpu",
                compute_type="int8",

            )

        return self.model
    # PROCESS AUDIO
    async def process_audio(
        self,
        audio_bytes: bytes,
        filename: str,
    ) -> dict:
        """
        Process uploaded interview audio.

        Returns:
            transcript
            audio_duration
            word_count
            speech_rate
        """

        if not audio_bytes:
            raise ValueError(
                "Audio file is empty."
            )

        
        # Create temporary audio file
        suffix = os.path.splitext(
            filename
        )[1] or ".webm"

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as temp_file:

                temp_file.write(
                    audio_bytes
                )

                temp_path = temp_file.name

            # Transcribe
            model = self._get_model()
            segments, info = model.transcribe(
                temp_path,
                beam_size=5,
            )

            segments = list(segments)

            transcript = " ".join(
                segment.text.strip()
                for segment in segments
                if segment.text.strip()
            ).strip()

          
            # Audio duration

            audio_duration = float(
                info.duration
            )
            # Word count
            word_count = len(
                transcript.split()
            )

            # Speech rate
            speech_rate = 0.0

            if audio_duration > 0:
                speech_rate = (
                    word_count
                    / audio_duration
                ) * 60

            return {
                "transcript": transcript,
                "audio_duration": round(
                    audio_duration,
                    2,
                ),
                "word_count": word_count,
                "speech_rate": round(
                    speech_rate,
                    2,
                ),
            }

        finally:

            # Remove temporary file
           
            if (
                temp_path
                and os.path.exists(temp_path)
            ):
                os.remove(
                    temp_path
                )