# MotionVox

MotionVox is a motion and voice-activated recording application built with Python and Tkinter. It allows users to record video and audio based on motion detection or audio triggers, with customizable settings for sensitivity, resolution, and output. The app supports both GUI and headless modes, making it versatile for desktop and server environments.

![MotionVox Demo](https://via.placeholder.com/800x400.png?text=MotionVox+Demo) <!-- Placeholder for demo image -->

## Features

- **Motion & Audio Detection**: Start recording based on motion or audio thresholds.
- **Customizable Settings**: Adjust resolution, FPS, motion/audio sensitivity, and silence timeout.
- **GUI & Headless Modes**: Use the intuitive Tkinter-based GUI or run in headless mode for server environments.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.
- **Logging & Status Updates**: Detailed logs and real-time status updates in the GUI.
- **Output Management**: Save recordings to a user-defined directory and easily access them.

## Installation

### Prerequisites

- Python 3.8+
- Tkinter (usually included with Python)
- Additional dependencies listed in `requirements.txt`

### Clone the Repository

```bash
git clone https://github.com/yourusername/motionvox.git
cd motionvox
```

### Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running in GUI Mode

Launch the application with the default GUI:

```bash
python motionvox.py
```

### Running in Headless Mode

Run the application without a GUI (ideal for servers or SSH sessions):

```bash
python motionvox.py --headless
```

### Command-Line Options

Customize the app's behavior with command-line arguments or environment variables:

```bash
python motionvox.py [options]
```

| Option                | Description                              | Example                          |
|-----------------------|------------------------------------------|----------------------------------|
| `--headless`          | Run in headless mode (no GUI)            | `python motionvox.py --headless` |
| `--output=DIR`        | Set output directory                     | `--output=/path/to/output`       |
| `--motion=N`          | Set motion threshold (1-100)             | `--motion=50`                    |
| `--audio=N`           | Set audio threshold (-60 to 0)           | `--audio=-30`                    |
| `--timeout=N`         | Set inactivity timeout (seconds)         | `--timeout=60`                   |
| `--resolution=W:H`    | Set resolution (width:height)            | `--resolution=1280:720`          |
| `--fps=N`             | Set frames per second                    | `--fps=30`                       |
| `--low-resource`      | Enable low-resource mode for SSH          | `--low-resource`                 |
| `--help`              | Show help message                        | `--help`                         |

### Environment Variables

You can also configure settings via environment variables:

```bash
export MOTIONVOX_OUTPUT_DIR="/path/to/output"
export MOTIONVOX_MOTION_THRESHOLD="50"
export MOTIONVOX_AUDIO_THRESHOLD="-30"
export MOTIONVOX_RESOLUTION="1280:720"
python motionvox.py
```

## GUI Overview

- **Start/Stop/Pause Buttons**: Control recording sessions.
- **Settings Dialog**: Configure video device, resolution, FPS, and silence timeout.
- **Output Folder Selection**: Choose where recordings are saved.
- **Status Bar**: Displays real-time updates and progress.
- **Info Log**: View timestamped logs of app activity.

## Headless Mode

In headless mode, the app runs without a GUI and outputs logs to the console. Use `Ctrl+C` to stop recording gracefully.

```bash
python motionvox.py --headless --output=/path/to/output
```

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter issues or have questions, please open an issue on the [GitHub Issues page](https://github.com/yourusername/motionvox/issues).

---

⭐️ If you find MotionVox useful, give us a star on GitHub!