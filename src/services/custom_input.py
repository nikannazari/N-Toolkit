"""
custom_input.py - Custom terminal input handler with arrow key support.
"""
import sys
import tty
import termios
import re

def _get_visible_len(s: str) -> int:
    """Calculate the visible length of a string, ignoring ANSI color codes."""
    return len(re.sub(r'\x1b\[[0-9;]*m', '', s))

class CustomInput:
    def __init__(self):
        self.history = []
        
    def get_input(self, prompt: str) -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        buffer = []
        cursor_pos = 0
        history_index = len(self.history)
        prompt_len = _get_visible_len(prompt)
        
        sys.stdout.write(prompt)
        sys.stdout.flush()
        
        try:
            # Set terminal to raw mode to capture individual keypresses
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                
                # ── Enter Key ──
                if ch in ('\r', '\n'):
                    sys.stdout.write('\r\n')
                    sys.stdout.flush()
                    cmd = ''.join(buffer)
                    if cmd:
                        self.history.append(cmd)
                    return cmd
                    
                # ── Ctrl+C ──
                elif ch == '\x03':
                    sys.stdout.write('\r\n')
                    sys.stdout.flush()
                    raise KeyboardInterrupt
                    
                # ── Ctrl+D ──
                elif ch == '\x04':
                    sys.stdout.write('\r\n')
                    sys.stdout.flush()
                    raise EOFError
                    
                # ── Escape Sequences (Arrows, PageUp/Down, Home, End) ──
                elif ch == '\x1b':
                    seq = sys.stdin.read(2)
                    
                    # Up Arrow OR PageUp
                    if seq == '[A' or seq == '[5~':
                        if self.history and history_index > 0:
                            history_index -= 1
                            buffer = list(self.history[history_index])
                            cursor_pos = len(buffer)
                            self._redraw(prompt, buffer, cursor_pos)
                            
                    # Down Arrow OR PageDown
                    elif seq == '[B' or seq == '[6~':
                        if self.history and history_index < len(self.history):
                            history_index += 1
                            if history_index == len(self.history):
                                buffer = []
                            else:
                                buffer = list(self.history[history_index])
                            cursor_pos = len(buffer)
                            self._redraw(prompt, buffer, cursor_pos)
                            
                    # Right Arrow
                    elif seq == '[C':
                        if cursor_pos < len(buffer):
                            cursor_pos += 1
                            self._redraw(prompt, buffer, cursor_pos)
                            
                    # Left Arrow
                    elif seq == '[D':
                        if cursor_pos > 0:
                            cursor_pos -= 1
                            self._redraw(prompt, buffer, cursor_pos)
                            
                    # Home Key
                    elif seq == '[H':
                        cursor_pos = 0
                        self._redraw(prompt, buffer, cursor_pos)
                        
                    # End Key
                    elif seq == '[F':
                        cursor_pos = len(buffer)
                        self._redraw(prompt, buffer, cursor_pos)
                            
                # ── Backspace ──
                elif ch in ('\x7f', '\x08'):
                    if cursor_pos > 0:
                        buffer.pop(cursor_pos - 1)
                        cursor_pos -= 1
                        self._redraw(prompt, buffer, cursor_pos)
                        
                # ── Normal Printable Character ──
                elif ch.isprintable():
                    buffer.insert(cursor_pos, ch)
                    cursor_pos += 1
                    self._redraw(prompt, buffer, cursor_pos)
                    
        finally:
            # Restore terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _redraw(self, prompt: str, buffer: list, cursor_pos: int):
        """Clears the current line and redraws the prompt and buffer."""
        # \r moves to the start of the line, \033[K clears from cursor to end of line
        sys.stdout.write('\r\033[K')
        sys.stdout.write(prompt + ''.join(buffer))
        
        # Calculate how many times to move the cursor left
        moves = len(buffer) - cursor_pos
        if moves > 0:
            sys.stdout.write(f'\033[{moves}D') # Move left by 'moves' columns
            
        sys.stdout.flush()