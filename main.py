import lxml
from lxml import etree
from lxml.etree import Element, SubElement
import os
import tkinter as tk
from tkinter import filedialog


## Removes leading spaces from the TCX file
def clean_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    cleaned_content = content.lstrip()
    with open(file_path, 'w') as f:
        f.write(cleaned_content)


## Parse the iFIT TCX file into an XML tree
def parse_xml(file_path):
    clean_file(file_path)
    return etree.parse(file_path)

## Reformat the iFIT TCX file to be more readable
def reformat_xml(xml_tree):
   def modify_xml(xml_tree):
    pretty_xml = etree.tostring(xml_tree, pretty_print=True)
    return etree.fromstring(pretty_xml)
   
## Modify the iFIT TCX file to replace the Activity with either Biking or Running
def modify_sport(xml_tree):
    # Get the user's choice
    print("Please select a sport:")
    print("1. Biking")
    print("2. Running")
    choice = input("Enter your choice (1 or 2): ")

    # Map the user's choice to a sport
    sport = "Biking" if choice == "1" else "Running"

    # Find the Sport attribute and set its value
    activity = xml_tree.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activity")
    if activity is not None:
        activity.set("Sport", sport)
    return xml_tree

## Replace the lap DistanceMeters with the final trackpoint DistanceMeters
def modify_lap_distance(xml_tree):
    lap = xml_tree.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap")
    if lap is not None:
        trackpoints = lap.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint")
        if trackpoints:
            final_trackpoint = trackpoints[-1]
            lap.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters").text = final_trackpoint.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters").text
    return xml_tree

## Set Lap Calories to an integer value
def modify_lap_calories(xml_tree):
    lap = xml_tree.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap")
    if lap is not None:
        calories = lap.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Calories")
        if calories is not None:
            # Convert the decimal value to an integer
            calories.text = str(int(float(calories.text)))
    return xml_tree

## update the averageheartratebpm to an integer value
def modify_average_heart_rate(xml_tree):
    ns = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    avg_heart_rate_elements = xml_tree.findall(".//ns:AverageHeartRateBpm/ns:Value", namespaces=ns)
    for elem in avg_heart_rate_elements:
        elem.text = str(int(float(elem.text)))
    return xml_tree

## update the Cadence in each trackpoint with its type. (similar to the HeartRateBpm)
def modify_trackpoint_cadence(xml_tree):
    trackpoints = xml_tree.findall(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint")
    for trackpoint in trackpoints:
        cadence = trackpoint.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Cadence")
        if cadence is not None:
            cadence.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CadenceValue_t")
    return xml_tree

##update the Watts in each trackpoint  to be a tpx extension value
def modify_trackpoint_watts(xml_tree):
    ns = {
        'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
        'tpx': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
    }
    trackpoints = xml_tree.findall(".//ns:Trackpoint", ns)
    for trackpoint in trackpoints:
        watts = trackpoint.find("ns:Watts", ns)
        if watts is not None:
            # Create the Extensions and TPX elements
            extensions = Element("{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Extensions")
            tpx = SubElement(extensions, "{http://www.garmin.com/xmlschemas/ActivityExtension/v2}TPX")
            
            # Move the Watts element to the TPX element
            watts.tag = "{http://www.garmin.com/xmlschemas/ActivityExtension/v2}Watts"
            tpx.append(watts)
            
            # Add the Extensions element to the Trackpoint element
            trackpoint.append(extensions)
    return xml_tree

## rename AverageWatts to AvgWatts and MaximumWatts to MaxWatts

def replace_average_watts(xml_tree):
    xml_string = etree.tostring(xml_tree, encoding='unicode')
    xml_string = xml_string.replace('AverageWatts', 'AvgWatts')
    xml_string = xml_string.replace('MaximumWatts', 'MaxWatts')
    xml_root = etree.fromstring(xml_string)
    xml_tree = etree.ElementTree(xml_root)  # Create a new ElementTree with the root element
    return xml_tree

## convert AvgWatts and MaxWatts to integer values
def convert_watts_to_int(xml_tree):
    avg_watts = xml_tree.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AvgWatts")
    if avg_watts is not None:
        # Convert the decimal value to an integer
        avg_watts.text = str(int(float(avg_watts.text)))

    max_watts = xml_tree.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaxWatts")
    if max_watts is not None:
        # Convert the decimal value to an integer
        max_watts.text = str(int(float(max_watts.text)))
    return xml_tree

## type the AvgWatts and MaxWatts in the lap as xsd:unsignedShort
def modify_lap_watts(xml_tree):
    lap = xml_tree.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap")
    if lap is not None:
        avg_watts = lap.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AvgWatts")
        if avg_watts is not None:
            avg_watts.set("{http://www.w3.org/2001/XMLSchema-instance}type", "xsd:unsignedShort")
        max_watts = lap.find(".//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaxWatts")
        if max_watts is not None:
            max_watts.set("{http://www.w3.org/2001/XMLSchema-instance}type", "xsd:unsignedShort")
    return xml_tree




def write_xml(xml_tree, file_path):
    xml_tree.write(file_path, pretty_print=True)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("TCX files", "*.tcx")])
    if not file_path:
        print("No file selected.")
        return

    xml_tree = parse_xml(file_path)
    reformat_xml(xml_tree)
    xml_tree = replace_average_watts(xml_tree)  # Capture the returned value
    modify_sport(xml_tree)
    modify_lap_distance(xml_tree)
    modify_lap_calories(xml_tree)
    modify_average_heart_rate(xml_tree)
    convert_watts_to_int(xml_tree)
    ## modify_lap_watts(xml_tree)
    modify_trackpoint_watts(xml_tree)
    modify_trackpoint_cadence(xml_tree)
    write_xml(xml_tree, file_path)  # Write the modified XML tree back to the file

if __name__ == "__main__":
    main()