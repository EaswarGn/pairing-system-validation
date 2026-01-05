# Checker Documentation

### app.py

This is the backend endpoint that the the client planA and planB send the generated pairings to. 

The /testcase endpoint accepts an index in the form of a GET request, named 'index', which is an integer between 1 and 412 inclusive of both 1 and 412. This represents which test case the backend app should return. There should be an impelmented session which starts at index=1, and increases each time correct pairings are sent to the other endpoint. The session should keep track of which test cases have apssed if it is to randomize the order of the test cases by randomizing the index. This endpoint uses the resolve_index() function to determine which test case(input) it should send to the user. The corresponding file is sent via flask.send_file and is in the .json format.

The /pairings endpoint accepts a post request with a file in the JSON, CSV or TRF format, or a raw JSON object sent to it. The endpoint resolves which test case solution to check the submitted pairings against with the resolve_testcase() function, which uses the name of the first section to find its solution. THE SECTION NAME SHOULD NOT BE RENAMED BY THE PAIRINGS-MAKING SOFTWARE; such action will cause the server to fail to resolve which solution to check the test case against. Once a file or object is received at the endpoint, the endpoint validates the file sent, checking for the appropriate format by checking if all the information is there, and, if valid, builds Section objects from the submitted pairings and the determined solutions file. Finally, it compares the submitted pairings' section objects with the solution pairings objects and return a verdict in the given format: [Verdict, 'Reason'], where Verdict is a boolean value which determines if the pairings are valid or not, and Reason is a string giving more detail on the verdict(e.g. which rule it failed for, 'All test cases passed', etc)

***Note*:** the CSV and TRF formats are not yet implemented, so the app only sends JSON files. In the future, a "format_index" could be implemented to specify which file format to fetch(JSON, CSV or TRF)

### Section.py

This is the file for a section objects whcih will process and check pairings for how many times they break the rules. The constructor loads in the information from a given JSON object.

The checkLastRound() function takes in a solution section object for that section to compare itself to, and returns a verdict of whether the submitted generated pairings are valid for that testcase. The method implements rule hierarchy (and soon its exceptions). If a submitted test case breaks any rule more than the solution file which has valid accepted pairings, then the submitted pairings are invalid and suboptimal, unless the pairings have broken a more important rule less times than the solution, which is unlikely. If the pairings are valid, the function returns a verdict in the given format: [Verdict, 'Reason'], where Verdict is a boolean value which determines if the pairings are valid or not, and Reason is a string giving more detail on the verdict(e.g. which rule it failed for, 'All test cases passed', etc)

The remaining methods return information relevant to rule-checking and individually check each rule, returning a list of which players in the pairings break that rule, and checkng if the Withdrawals/Byes listed are actually implemented in the pairings. They are used by the checkLastRound() function to determine if the submitted test case breaks the rules more than the solution.

The get functions somply return information about the object, specifically the players, the teams, and a dictionary of the object information just as it was inputted in valid JSON format and ready to be converted to it.

### Player.py

This file contains the Player class which facilitates rule-checking in Section.py by taking in player information relayed by Section.py and creating player objects. Player object methods return useful information about the players in the desired format, which simplifies the code in Sections.py by making it cleaner and more compree=hensible.

### Team.py

Just like Player.py, Team.py creates Team objects that facilitate Team functionality in pairings in Section.py. The class contains helper methods and methods returning useful information relevant to pairings rule-checking

### convert.py

convert.py is a file containing helper functions. such as format validation methods and section-building functions, which convert a validly-formatted file to Section objects which are then used to compare pairings with the solution.

TODO: CSV and TRF formats are not implemented
