# iFIT TCX File Converter

## Description
This project is aimed at developing a TCX file converter for use with the iFIT S22i such that the files provide maximum compaitbility with Garmin Connect.

## Features
- Replaces the Activity type of 'Other' with a user selectable "Biking' or 'Running'
- Replaces the Lap Distance with the distance from the final Trackpoint. 
- Sets Calories, Heart Rate, and Cadence to the appropriate types for use by Connect
- Updates the Watts walue to be a TPX extension within each trackpoint. 

## Installation
1. Clone the repository: `git clone https://github.com/douglas-christian/iFIT-TCX-Converter.git`
2. Install dependencies: `pip install lxml`, `pip install tinkter`, `pip install os`
3. Run main.py.
4. An exexutable is supplied if you would prefer not to install python.

## Usage
1. Download your TCX file from iFIT. (Make a Copy if you would like to compare it to the final output.)
2. Run the executable or included Python script.
3. Use the File Finder to select your TCX file.
4. Select either Biking or Running.th the application.
5. Your TCX file is edited in place and reformatted.
6. Upload your new TCX file to Garmin Connect and be amazed.

## Contributing
Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact
For any inquiries or support, please contact the project maintainer at [@douglas-christian].
