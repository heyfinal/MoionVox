self._append_info(f"Output Directory: {self.output_directory}")
        self._append_info("Starting dependency installation and initialization...")
        self._append_info("Please wait while the application initializes...")
        
        # Status bar
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Disable controls until initialization complete
        self._disable_controls()
        
    def _disable_controls(self):
        """Disable all controls"""
        self.start_btn.state(['disabled'])
        self.stop_btn.state(['disabled'])
        self.pause_btn.state(['disabled'])
        self.settings_btn.state(['disabled'])
        self.folder_btn.state(['disabled'])
        self.view_btn.state(['disabled'])
        
    def _enable_controls(self):
        """Enable controls after initialization"""
        self.start_btn.state(['!disabled'])
        self.settings_btn.state(['!disabled'])
        self.folder_btn.state(['!disabled'])
        self.view_btn.state(['!disabled'])
        
    def _update_status_bar(self, message, progress=None):
        """Update the status bar with a message and optional progress"""
        logger.info(message)
        self.status_bar.set_status(message, progress)
        self._append_info(message)
        
    def _append_info(self, message):
        """Append a message to the info text widget"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, formatted_message)
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)
        
    def _update_motion_sensitivity(self, value):
        """Update motion sensitivity value"""
        value = int(float(value))
        self.motion_label.config(text=str(value))
        self.recording_engine.motion_threshold = value
        
    def _update_audio_sensitivity(self, value):
        """Update audio sensitivity value"""
        value = int(float(value))
        db_value = -60 + value  # Convert to dB (-60 to 0)
        self.audio_label.config(text=f"{db_value} dB")
        self.recording_engine.audio_threshold = db_value
        
    def _start_recording(self):
        """Start recording"""
        self.recording_engine.output_directory = self.output_directory
        success = self.recording_engine.start_recording()
        
        if success:
            self._append_info("Recording started")
            self.start_btn.state(['disabled'])
            self.stop_btn.state(['!disabled'])
            self.pause_btn.state(['!disabled'])
            self.settings_btn.state(['disabled'])
        else:
            self._append_info("Failed to start recording")
            
    def _stop_recording(self):
        """Stop recording"""
        self.recording_engine.stop_recording()
        self._append_info("Recording stopped")
        
        self.start_btn.state(['!disabled'])
        self.stop_btn.state(['disabled'])
        self.pause_btn.state(['disabled'])
        self.pause_btn.config(text="Pause")
        self.settings_btn.state(['!disabled'])
        
    def _toggle_pause(self):
        """Toggle pause/resume recording"""
        if self.recording_engine.paused:
            self.recording_engine.resume_recording()
            self._append_info("Recording resumed")
            self.pause_btn.config(text="Pause")
        else:
            self.recording_engine.pause_recording()
            self._append_info("Recording paused")
            self.pause_btn.config(text="Resume")
            
    def _show_settings(self):
        """Show advanced settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Advanced Settings")
        settings_window.geometry("500x400")
        settings_window.minsize(400, 300)
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Apply SV-TTK theme
        sv_ttk.set_theme("dark")
        
        # Add padding
        frame = ttk.Frame(settings_window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add settings
        ttk.Label(frame, text="Video Device:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        video_device_var = tk.IntVar(value=self.recording_engine.video_device)
        video_device_entry = ttk.Spinbox(
            frame, from_=0, to=10, 
            textvariable=video_device_var, width=5
        )
        video_device_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(frame, text="Resolution:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        resolution_options = ["640x480", "1280x720", "1920x1080"]
        current_resolution = f"{self.recording_engine.resolution[0]}x{self.recording_engine.resolution[1]}"
        
        resolution_var = tk.StringVar(value=current_resolution)
        resolution_combo = ttk.Combobox(
            frame, values=resolution_options,
            textvariable=resolution_var, width=10
        )
        resolution_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(frame, text="FPS:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        
        fps_options = ["15", "30", "60"]
        fps_var = tk.StringVar(value=str(self.recording_engine.fps))
        fps_combo = ttk.Combobox(
            frame, values=fps_options,
            textvariable=fps_var, width=5
        )
        fps_combo.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(frame, text="Silence Timeout (seconds):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        
        timeout_var = tk.IntVar(value=self.recording_engine.silence_timeout)
        timeout_entry = ttk.Spinbox(
            frame, from_=5, to=300, increment=5,
            textvariable=timeout_var, width=5
        )
        timeout_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # Save button
        def save_settings():
            try:
                # Update video device
                self.recording_engine.video_device = video_device_var.get()
                
                # Update resolution
                res_parts = resolution_var.get().split('x')
                width = int(res_parts[0])
                height = int(res_parts[1])
                self.recording_engine.resolution = (width, height)
                
                # Update FPS
                self.recording_engine.fps = int(fps_var.get())
                
                # Update timeout
                self.recording_engine.silence_timeout = timeout_var.get()
                
                self._append_info("Settings updated")
                settings_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
                
        ttk.Button(
            frame, text="Save Settings",
            command=save_settings
        ).grid(row=4, column=0, columnspan=2, padx=5, pady=20)
        
    def _select_output_folder(self):
        """Select output folder for recordings"""
        directory = filedialog.askdirectory(
            initialdir=self.output_directory,
            title="Select Output Folder"
        )
        
        if directory:
            self.output_directory = directory
            self._append_info(f"Output directory changed to: {directory}")
            
    def _view_recordings(self):
        """Open the output directory in file explorer"""
        if os.path.exists(self.output_directory):
            # Open folder based on platform
            if sys.platform == 'win32':
                os.startfile(self.output_directory)
            elif sys.platform == 'darwin':  # macOS
                subprocess.call(['open', self.output_directory])
            else:  # Linux
                subprocess.call(['xdg-open', self.output_directory])
        else:
            messagebox.showerror(
                "Directory Not Found",
                f"The directory {self.output_directory} does not exist."
            )


def main():
    """Main entry point for the application"""
    try:
        # Check if DISPLAY is available (for SSH with X forwarding)
        headless_mode = False
        if sys.platform != 'win32' and os.environ.get('DISPLAY') is None:
            logger.info("No display detected. Running in headless mode.")
            headless_mode = True
        
        if not headless_mode:
            # Set up exception handling for GUI mode
            def show_error(exc_type, exc_value, exc_traceback):
                """Show error dialog for uncaught exceptions"""
                error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                logger.critical(f"Uncaught exception: {error_msg}")
                
                messagebox.showerror(
                    "Error",
                    f"An unexpected error occurred: {exc_value}\n\n"
                    f"Please check the log file: {log_file}"
                )
                
            # Set up global exception handler
            sys.excepthook = show_error
            
            # Create root window
            root = tk.Tk()
            
            # Initialize application
            app = MotionVoxApp(root)
            
            # Set up clean shutdown on exit
            def on_closing():
                """Handle window closing"""
                if hasattr(app, 'recording_engine') and app.recording_engine.running:
                    if messagebox.askyesno("Exit", "Recording is in progress. Stop recording and exit?"):
                        app.recording_engine.stop_recording()
                        root.destroy()
                else:
                    root.destroy()
                    
            root.protocol("WM_DELETE_WINDOW", on_closing)
            
            # Start main loop
            root.mainloop()
        else:
            # Headless mode operation
            print("MotionVox - Headless Mode")
            print(f"Log file: {log_file}")
            
            # Command line arguments
            output_dir = os.environ.get('MOTIONVOX_OUTPUT_DIR', os.path.expanduser("~/Documents/MotionVox Recordings"))
            os.makedirs(output_dir, exist_ok=True)
            print(f"Output directory: {output_dir}")
            
            # Create headless recording engine
            engine = RecordingEngine(output_dir, status_callback=print)
            
            # Set parameters from environment variables
            engine.motion_threshold = int(os.environ.get('MOTIONVOX_MOTION_THRESHOLD', '30'))
            engine.audio_threshold = int(os.environ.get('MOTIONVOX_AUDIO_THRESHOLD', '-30'))
            engine.silence_timeout = int(os.environ.get('MOTIONVOX_TIMEOUT', '60'))
            engine.fps = int(os.environ.get('MOTIONVOX_FPS', '30'))
            
            if ':' in os.environ.get('MOTIONVOX_RESOLUTION', '1280:720'):
                width, height = os.environ.get('MOTIONVOX_RESOLUTION').split(':')
                engine.resolution = (int(width), int(height))
            
            # Initialize
            if not engine.initialize():
                print("Failed to initialize recording engine")
                sys.exit(1)
            
            print("Starting recording (Press Ctrl+C to stop)...")
            engine.start_recording()
            
            # Set up signal handler for clean shutdown
            def signal_handler(sig, frame):
                print("\nStopping recording...")
                engine.stop_recording()
                print("Recording stopped. Exiting.")
                sys.exit(0)
                
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            # Keep the main thread alive
            while engine.running:
                time.sleep(1)
            
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        if not headless_mode:
            messagebox.showerror(
                "Fatal Error",
                f"A fatal error occurred: {str(e)}\n\n"
                f"Please check the log file: {log_file}"
            )
        else:
            print(f"Fatal error: {str(e)}")
            print(f"Check log file: {log_file}")


if __name__ == "__main__":
    # Parse command line arguments for SSH mode
    if len(sys.argv) > 1:
        # Simple command line argument handling
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("MotionVox - Motion & Voice Activated Recording App")
            print("Usage:")
            print("  python motionvox.py [options]")
            print("\nOptions:")
            print("  --headless         Run in headless mode (no GUI)")
            print("  --output=DIR       Set output directory")
            print("  --motion=N         Set motion threshold (1-100)")
            print("  --audio=N          Set audio threshold (-60 to 0)")
            print("  --timeout=N        Set inactivity timeout in seconds")
            print("  --low-resource     Enable low resource mode for SSH sessions")
            print("  --help             Show this help message")
            print("\nEnvironment Variables:")
            print("  MOTIONVOX_OUTPUT_DIR     Output directory")
            print("  MOTIONVOX_MOTION_THRESHOLD  Motion sensitivity (1-100)")
            print("  MOTIONVOX_AUDIO_THRESHOLD   Audio sensitivity (-60 to 0)")
            print("  MOTIONVOX_TIMEOUT        Inactivity timeout in seconds")
            print("  MOTIONVOX_LOW_RESOURCE   Set to 1 for low resource mode")
            print("  MOTIONVOX_RESOLUTION     Format: width:height (e.g. 640:480)")
            print("  MOTIONVOX_FPS            Frames per second")
            print("  MOTIONVOX_HEARTBEAT      Heartbeat interval in seconds")
            sys.exit(0)
        
        # Process command line arguments
        for arg in sys.argv[1:]:
            if arg == "--headless":
                os.environ['DISPLAY'] = ''  # Force headless mode
            elif arg.startswith("--output="):
                os.environ['MOTIONVOX_OUTPUT_DIR'] = arg.split('=', 1)[1]
            elif arg.startswith("--motion="):
                os.environ['MOTIONVOX_MOTION_THRESHOLD'] = arg.split('=', 1)[1]
            elif arg.startswith("--audio="):
                os.environ['MOTIONVOX_AUDIO_THRESHOLD'] = arg.split('=', 1)[1]
            elif arg.startswith("--timeout="):
                os.environ['MOTIONVOX_TIMEOUT'] = arg.split('=', 1)[1]
            elif arg == "--low-resource":
                os.environ['MOTIONVOX_LOW_RESOURCE'] = '1'
            elif arg.startswith("--resolution="):
                # Format: width:height (e.g. 640:480)
                resolution = arg.split('=', 1)[1]
                os.environ['MOTIONVOX_RESOLUTION'] = resolution.replace('x', ':')
            elif arg.startswith("--fps="):
                os.environ['MOTIONVOX_FPS'] = arg.split('=', 1)[1]
            elif arg.startswith("--heartbeat="):
                os.environ['MOTIONVOX_HEARTBEAT'] = arg.split('=', 1)[1]
    
    # Check if running in SSH session and set low-resource mode automatically
    if os.environ.get('SSH_CLIENT') and os.environ.get('MOTIONVOX_LOW_RESOURCE') is None:
        print("SSH session detected. Enabling low-resource mode by default.")
        print("To disable, set MOTIONVOX_LOW_RESOURCE=0 before running.")
        os.environ['MOTIONVOX_LOW_RESOURCE'] = '1'
    
    # Start the application
    main()
                
