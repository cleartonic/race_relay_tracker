# Race / Relay Tracker

This is a standalone application that keeps track of segments, teams with a simple layout. It is designed for OBS Window Capture use via a 480x360 application layout.

# Features
- Keeps track of any number of segments
- Allows up to four teams/racers to be tracked

# Download
Please use the [latest Release](https://github.com/cleartonic/race_relay_tracker/releases) for the initial download.

# Setup
All configurations are either set up in the `config.yml` file, or in the application itself. Use a text editor to open this file, and change the parameters.  

The configuration file is set up for an initial run. Please adhere to the same format for each field. For example, `team_names: ["Team A", "Team B", "Team C", "Team D"]` should be kept in this format of `team_names: ["A", "B", "C", "D"]`. 

Any image can be used for team icons, though the default is set to 32x32px. Anything over 50x50px will be shrunk. 

Right click -> Settings for additional settings in the application. Settings will not be saved to the `config.yml` file automatically, so you will have to manually edit this file to save changes you make. 

The segments area can be scrolled using the mouse wheel. There is an option to enable up/down buttons in the Settings menu. 

# Credits
Created by [cleartonic](https://cleartonic.net/)