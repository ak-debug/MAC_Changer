# MAC Changer

MAC Changer is a Python script with a graphical user interface (GUI) built using Tkinter. It allows users to change and restore the Media Access Control (MAC) address of a network interface on a Linux system.

## Prerequisites

- Python 3.x
- Tkinter library
- netifaces library

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/mac-changer.git
   ```

2. Install the required dependencies:

   ```
   pip install netifaces
   ```

## Usage

1. Open a terminal and navigate to the project directory:

   ```
   cd mac-changer
   ```

2. Run the script:

   ```
   python mac_changer.py
   ```

3. The MAC Changer GUI will appear, allowing you to change and restore MAC addresses.

## Features

- **Change MAC Address**: Enter a custom MAC address or leave it blank to generate a random MAC address. Click the "Change" button to change the MAC address of the selected network interface.
- **Restore Original MAC**: Click the "Restore" button to restore the original MAC address of the selected network interface.
- **Automatic MAC Changes**: Enable automatic MAC changes by clicking "File" > "Settings" and selecting the "Enable automatic MAC changes" checkbox. Specify the change interval in seconds and click "Save". The MAC address will be changed automatically at the specified interval.
- **Result Box**: The result box displays the outcome of MAC address changes and restorations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or bug fixes.

## Acknowledgments

This script utilizes the netifaces library to fetch network interface information and the subprocess module for executing system commands.

## Disclaimer

Changing MAC addresses without proper authorization may be against the terms of service of your network or system. Use this script responsibly and for educational purposes only.

Feel free to customize and enhance the README to provide more information or instructions specific to your code and its usage.