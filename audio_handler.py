"""
Audio Handler for Aphasia Object Recognition System
Handles text-to-speech functionality using espeak.
"""

import subprocess
import logging
import threading
from config import TTS_COMMAND, TTS_PITCH, TTS_SPEED, TTS_VOLUME

class AudioHandler:
    """Handles text-to-speech audio output."""
    
    def __init__(self):
        """Initialize the audio handler."""
        self.logger = logging.getLogger(__name__)
        self.is_speaking = False
        
        # Test if espeak is available
        try:
            subprocess.run([TTS_COMMAND, '--version'], 
                         capture_output=True, check=True, timeout=5)
            self.logger.info("espeak is available")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            self.logger.warning("espeak not found or not working properly")
    
    def speak(self, text, blocking=False):
        """
        Convert text to speech using espeak.
        
        Args:
            text (str): Text to speak
            blocking (bool): If True, wait for speech to complete. If False, speak in background.
        
        Returns:
            bool: True if speech was initiated successfully, False otherwise
        """
        if not text or not text.strip():
            self.logger.warning("Empty text provided for speech")
            return False
        
        # Clean the text for better speech
        clean_text = self._clean_text_for_speech(text)
        
        if blocking:
            return self._speak_blocking(clean_text)
        else:
            return self._speak_non_blocking(clean_text)
    
    def _clean_text_for_speech(self, text):
        """
        Clean text to make it more suitable for speech synthesis.
        
        Args:
            text (str): Original text
            
        Returns:
            str: Cleaned text
        """
        # Replace underscores with spaces
        clean_text = text.replace('_', ' ')
        
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        
        # Capitalize first letter for better pronunciation
        if clean_text:
            clean_text = clean_text[0].upper() + clean_text[1:]
        
        return clean_text
    
    def _speak_blocking(self, text):
        """
        Speak text and wait for completion.
        
        Args:
            text (str): Text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.is_speaking = True
            self.logger.info(f"Speaking (blocking): '{text}'")
            
            # Build espeak command with parameters
            cmd = [
                TTS_COMMAND,
                f'-p{TTS_PITCH}',  # Pitch
                f'-s{TTS_SPEED}',  # Speed
                f'-a{TTS_VOLUME}', # Volume
                text
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            
            if result.returncode == 0:
                self.logger.debug("Speech completed successfully")
                return True
            else:
                self.logger.error(f"espeak failed with return code {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Speech timeout")
            return False
        except Exception as e:
            self.logger.error(f"Error during speech: {e}")
            return False
        finally:
            self.is_speaking = False
    
    def _speak_non_blocking(self, text):
        """
        Speak text in a separate thread without blocking.
        
        Args:
            text (str): Text to speak
            
        Returns:
            bool: True if thread was started successfully, False otherwise
        """
        try:
            if self.is_speaking:
                self.logger.warning("Already speaking, skipping new speech request")
                return False
            
            # Start speech in a separate thread
            speech_thread = threading.Thread(
                target=self._speak_blocking,
                args=(text,),
                daemon=True
            )
            speech_thread.start()
            
            self.logger.debug(f"Started non-blocking speech: '{text}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting speech thread: {e}")
            return False
    
    def is_currently_speaking(self):
        """
        Check if currently speaking.
        
        Returns:
            bool: True if currently speaking, False otherwise
        """
        return self.is_speaking
    
    def stop_speech(self):
        """Stop any ongoing speech (best effort)."""
        try:
            # Kill any running espeak processes
            subprocess.run(['pkill', 'espeak'], capture_output=True)
            self.is_speaking = False
            self.logger.info("Speech stopped")
        except Exception as e:
            self.logger.error(f"Error stopping speech: {e}")
