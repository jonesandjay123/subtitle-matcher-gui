"""
GUI Module - Tkinter-based interface for Subtitle Matcher
Provides a simple, intuitive interface for subtitle alignment.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from pathlib import Path
import threading

from gemini_client import GeminiClient
from utils.config import Config
from utils.file_ops import read_srt_file, write_srt_file


class SubtitleMatcherGUI:
    """Main GUI application class using Tkinter."""

    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Gemini Subtitle Matcher")
        self.root.geometry("1000x850")
        self.root.resizable(True, True)

        # Configuration
        self.config = Config()

        # Variables
        self.input_srt_path = tk.StringVar()
        self.output_srt_path = tk.StringVar()
        self.api_key = tk.StringVar(value=self.config.get_api_key())
        self.status_text = tk.StringVar(value="Ready")

        # Gemini client
        self.gemini_client = None

        # Build UI
        self._build_ui()

    def _build_ui(self):
        """Build the complete user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        current_row = 0

        # === API Key Section ===
        ttk.Label(main_frame, text="Gemini API Key:", font=("", 10, "bold")).grid(
            row=current_row, column=0, sticky=tk.W, pady=(0, 5)
        )
        current_row += 1

        api_key_frame = ttk.Frame(main_frame)
        api_key_frame.grid(row=current_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        api_key_frame.columnconfigure(0, weight=1)

        self.api_key_entry = ttk.Entry(api_key_frame, textvariable=self.api_key, show="*", width=50)
        self.api_key_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        # Add right-click context menu for API key entry
        self._create_context_menu_for_entry(self.api_key_entry)

        ttk.Button(api_key_frame, text="Show", command=self._toggle_api_key_visibility).grid(
            row=0, column=1
        )

        if not self.api_key.get():
            ttk.Label(main_frame, text="⚠️ API key not found in environment. Please enter manually.",
                     foreground="orange").grid(row=current_row+1, column=0, columnspan=3, sticky=tk.W)
            current_row += 1

        current_row += 1

        # === Separator ===
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(
            row=current_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        current_row += 1

        # === Input SRT File ===
        ttk.Label(main_frame, text="Original SRT File:", font=("", 10, "bold")).grid(
            row=current_row, column=0, sticky=tk.W, pady=(0, 5)
        )
        current_row += 1

        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=current_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)

        ttk.Entry(input_frame, textvariable=self.input_srt_path, state="readonly").grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(input_frame, text="Browse...", command=self._browse_input_file).grid(
            row=0, column=1
        )
        current_row += 1

        # === Corrected Transcript ===
        ttk.Label(main_frame, text="Corrected Transcript:", font=("", 10, "bold")).grid(
            row=current_row, column=0, sticky=tk.W, pady=(0, 5)
        )
        current_row += 1

        # Scrolled text widget for transcript
        self.transcript_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=10,
            font=("", 10)
        )
        self.transcript_text.grid(
            row=current_row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )
        main_frame.rowconfigure(current_row, weight=1)

        # Add right-click context menu for transcript text
        self._create_context_menu(self.transcript_text)

        current_row += 1

        # === Output SRT File ===
        ttk.Label(main_frame, text="Output SRT File (optional):", font=("", 10, "bold")).grid(
            row=current_row, column=0, sticky=tk.W, pady=(0, 5)
        )
        current_row += 1

        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=current_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)

        ttk.Entry(output_frame, textvariable=self.output_srt_path).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(output_frame, text="Browse...", command=self._browse_output_file).grid(
            row=0, column=1
        )
        current_row += 1

        ttk.Label(main_frame, text="(Leave empty to save in the same folder as input)",
                 foreground="gray").grid(row=current_row, column=0, columnspan=3, sticky=tk.W)
        current_row += 1

        # === Run Button ===
        self.run_button = ttk.Button(
            main_frame,
            text="🚀 Run Subtitle Matching",
            command=self._run_matching,
            style="Accent.TButton"
        )
        self.run_button.grid(row=current_row, column=0, columnspan=3, pady=15)
        current_row += 1

        # === Progress Bar ===
        self.progress_bar = ttk.Progressbar(main_frame, mode="indeterminate", length=300)
        self.progress_bar.grid(row=current_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        current_row += 1

        # === Status Label ===
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_text,
            font=("", 9),
            foreground="blue"
        )
        status_label.grid(row=current_row, column=0, columnspan=3, sticky=tk.W)
        current_row += 1

        # === Log Display ===
        ttk.Label(main_frame, text="Processing Log:", font=("", 10, "bold")).grid(
            row=current_row, column=0, sticky=tk.W, pady=(10, 5)
        )
        current_row += 1

        # Log text widget with scrollbar
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=8,
            font=("Courier", 9),
            state="disabled",
            bg="#1e1e1e",
            fg="#e0e0e0",
            insertbackground="white"
        )
        self.log_text.grid(
            row=current_row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )
        main_frame.rowconfigure(current_row, weight=1)

    def _create_context_menu_for_entry(self, entry_widget):
        """Create right-click context menu for Entry widget with copy/paste support."""
        context_menu = tk.Menu(entry_widget, tearoff=0)

        context_menu.add_command(
            label="Cut (⌘X)",
            command=lambda: self._context_cut(entry_widget)
        )
        context_menu.add_command(
            label="Copy (⌘C)",
            command=lambda: self._context_copy(entry_widget)
        )
        context_menu.add_command(
            label="Paste (⌘V)",
            command=lambda: self._context_paste(entry_widget)
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="Select All (⌘A)",
            command=lambda: self._context_select_all_entry(entry_widget)
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="Clear",
            command=lambda: entry_widget.delete(0, tk.END)
        )

        # Bind right-click to show menu
        entry_widget.bind("<Button-2>", lambda e: context_menu.tk_popup(e.x_root, e.y_root))
        entry_widget.bind("<Button-3>", lambda e: context_menu.tk_popup(e.x_root, e.y_root))

    def _create_context_menu(self, text_widget):
        """Create right-click context menu for text widget with copy/paste support."""
        context_menu = tk.Menu(text_widget, tearoff=0)

        context_menu.add_command(
            label="Cut (⌘X)",
            command=lambda: self._context_cut(text_widget)
        )
        context_menu.add_command(
            label="Copy (⌘C)",
            command=lambda: self._context_copy(text_widget)
        )
        context_menu.add_command(
            label="Paste (⌘V)",
            command=lambda: self._context_paste(text_widget)
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="Select All (⌘A)",
            command=lambda: self._context_select_all(text_widget)
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="Clear",
            command=lambda: text_widget.delete("1.0", tk.END)
        )

        # Bind right-click to show menu
        text_widget.bind("<Button-2>", lambda e: context_menu.tk_popup(e.x_root, e.y_root))
        text_widget.bind("<Button-3>", lambda e: context_menu.tk_popup(e.x_root, e.y_root))

    def _context_cut(self, text_widget):
        """Cut selected text to clipboard."""
        try:
            text_widget.event_generate("<<Cut>>")
        except:
            pass

    def _context_copy(self, text_widget):
        """Copy selected text to clipboard."""
        try:
            text_widget.event_generate("<<Copy>>")
        except:
            pass

    def _context_paste(self, text_widget):
        """Paste text from clipboard."""
        try:
            text_widget.event_generate("<<Paste>>")
        except:
            pass

    def _context_select_all(self, text_widget):
        """Select all text in Text widget."""
        text_widget.tag_add(tk.SEL, "1.0", tk.END)
        text_widget.mark_set(tk.INSERT, "1.0")
        text_widget.see(tk.INSERT)

    def _context_select_all_entry(self, entry_widget):
        """Select all text in Entry widget."""
        entry_widget.select_range(0, tk.END)
        entry_widget.icursor(tk.END)

    def _toggle_api_key_visibility(self):
        """Toggle API key visibility between masked and visible."""
        current_show = self.api_key_entry.cget("show")
        if current_show == "*":
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")

    def _browse_input_file(self):
        """Open file dialog to select input SRT file."""
        filename = filedialog.askopenfilename(
            title="Select Original SRT File",
            filetypes=[("SRT Files", "*.srt"), ("All Files", "*.*")]
        )
        if filename:
            self.input_srt_path.set(filename)
            # Auto-suggest output path
            if not self.output_srt_path.get():
                input_path = Path(filename)
                suggested_output = input_path.parent / f"{input_path.stem}_matched.srt"
                self.output_srt_path.set(str(suggested_output))

    def _browse_output_file(self):
        """Open file dialog to select output SRT file location."""
        filename = filedialog.asksaveasfilename(
            title="Save Matched SRT File As",
            defaultextension=".srt",
            filetypes=[("SRT Files", "*.srt"), ("All Files", "*.*")]
        )
        if filename:
            self.output_srt_path.set(filename)

    def _validate_inputs(self):
        """
        Validate all inputs before processing.
        Returns (is_valid, error_message)
        """
        # Check API key
        api_key = self.api_key.get().strip()
        if not api_key:
            return False, "Please enter your Gemini API key."

        # Check input SRT file
        input_path = self.input_srt_path.get()
        if not input_path:
            return False, "Please select an original SRT file."

        if not os.path.exists(input_path):
            return False, f"Input file not found: {input_path}"

        # Check corrected transcript
        transcript = self.transcript_text.get("1.0", tk.END).strip()
        if not transcript:
            return False, "Please paste your corrected transcript."

        return True, None

    def _log(self, message):
        """Add a log message to the log display (thread-safe)."""
        def append_log():
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)  # Auto-scroll to bottom
            self.log_text.config(state="disabled")

        self.root.after(0, append_log)

    def _clear_log(self):
        """Clear the log display."""
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")

    def _run_matching(self):
        """Main function to run the subtitle matching process."""
        # Validate inputs
        is_valid, error_msg = self._validate_inputs()
        if not is_valid:
            messagebox.showerror("Input Error", error_msg)
            return

        # Clear previous logs
        self._clear_log()
        self._log("=" * 60)
        self._log("🚀 Starting subtitle matching process...")
        self._log("=" * 60)

        # Disable button during processing
        self.run_button.config(state="disabled")
        self.progress_bar.start(10)
        self.status_text.set("Processing...")

        # Run in separate thread to keep GUI responsive
        thread = threading.Thread(target=self._process_matching, daemon=True)
        thread.start()

    def _process_matching(self):
        """
        Process the subtitle matching in a background thread.
        This prevents GUI freezing during API calls.
        """
        try:
            # Read input SRT file
            self._update_status("Reading original SRT file...")
            self._log("\n📂 Reading input SRT file...")
            input_path = self.input_srt_path.get()
            self._log(f"   Input: {input_path}")
            original_srt_content = read_srt_file(input_path)
            self._log(f"   ✓ Loaded {len(original_srt_content)} characters")

            # Get corrected transcript
            corrected_transcript = self.transcript_text.get("1.0", tk.END).strip()
            self._log(f"\n📝 Corrected transcript: {len(corrected_transcript)} characters")

            # Initialize Gemini client with API key
            self._update_status("Connecting to Gemini API...")
            self._log("\n🔗 Initializing Gemini API client...")
            api_key = self.api_key.get().strip()
            self.gemini_client = GeminiClient(api_key, log_callback=self._log)
            self._log("   ✓ Client initialized successfully")

            # Call Gemini API to align subtitles
            self._update_status("Processing with Gemini 2.5 Flash...")
            self._log("\n🤖 Calling Gemini 2.5 Flash API...")
            self._log("   Model: gemini-2.5-flash")
            self._log("   This may take 10-30 seconds depending on content length...")

            matched_srt = self.gemini_client.align_subtitles(
                original_srt_content,
                corrected_transcript
            )

            self._log(f"   ✓ Received response: {len(matched_srt)} characters")

            # Determine output path
            output_path = self.output_srt_path.get()
            if not output_path:
                input_path_obj = Path(input_path)
                output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_matched.srt")

            # Write output SRT file
            self._update_status("Writing matched SRT file...")
            self._log(f"\n💾 Writing output file...")
            self._log(f"   Output: {output_path}")
            write_srt_file(output_path, matched_srt)
            self._log("   ✓ File saved successfully")

            # Success!
            self._update_status("✅ Complete!")
            self._log("\n" + "=" * 60)
            self._log("✅ Subtitle matching completed successfully!")
            self._log("=" * 60)

            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Subtitle matching completed!\n\nOutput saved to:\n{output_path}"
            ))

        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            self._log(f"\n❌ ERROR: {error_msg}")
            self._log("=" * 60)
            self._update_status("❌ Error occurred")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

        finally:
            # Re-enable button and stop progress bar
            self.root.after(0, self._reset_ui)

    def _update_status(self, message):
        """Thread-safe status update."""
        self.root.after(0, lambda: self.status_text.set(message))

    def _reset_ui(self):
        """Reset UI elements after processing."""
        self.run_button.config(state="normal")
        self.progress_bar.stop()

    def run(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()
