from flask import Flask
from flask import Flask, request, send_file
from flask_cors import CORS
from convert import *
import os

app = Flask(__name__)
CORS(app)

@app.route('/pairings', methods=['POST'])
def pairings():
    print("Request has reached the server: ", request)
    print(request.content_type)

    if(request.content_type != 'application/json'):
        index = int(request.form.get('index'))
    else:
        index = request.json.get('index')
    print("the index is ", index)
    # Get the pairings file
    content_type = request.content_type

    if content_type.startswith('multipart/form-data'):
        print("Request is multipart")
        generated_pairings_file = request.files['file']

        file_extension = os.path.splitext(generated_pairings_file.filename)[1]
        section_results = []

        # JSON Files
        if file_extension.lower() == '.json':
            # Load JSON and validate it
            generated_pairings = json.loads(generated_pairings_file.read())

            if validateJSONFormat(generated_pairings):
                sections = build_sections_from_JSON(generated_pairings)
                print("Poggers Request has reached the server: ", request)

                # Load solutions file and create solution object

                solution_file = resolve_testcase_index(index)
                if solution_file == "Invalid Test Case: Test case was not found. Make sure the section name is unchanged":
                    print("Invalid Test Case: Test case was not found. Make sure the section name is unchanged")
                    return "Invalid Test Case: Test case was not found. Make sure the section name is unchanged"
                elif solution_file != resolve_testcase(sections[0].name):
                    print("Invalid Test Case: Incorrect pairings file provided for the prompted testcase")
                    return "Invalid Test Case: Incorrect pairings file provided for the prompted testcase"
                with open(solution_file) as f:
                    solution_object = json.loads(f.read())
                solutions = [Section(section) for section in solution_object['Sections']]


                for i in range(len(sections)):
                    section_results.append(sections[i].checkLastRound(solutions[i]))

                print("DONEEEEE",section_results)
            else:
                return 'Invalid JSON file'
            




        # CSV Files
        elif file_extension.lower() == '.csv':
            # Process CSV file
            if validateCSVFormat(generated_pairings):
                sections = build_sections_from_CSV(generated_pairings)
            else:
                return 'Invalid CSV file'
            



        # TRF Files
        elif file_extension.lower() == '.trf':
            # Process TRF file
            if validateTRFFormat(generated_pairings):
                sections = build_sections_from_TRF(generated_pairings)
            else:
                return 'Invalid TRF file'
        else:
            return 'Unknown file type'
        
        return section_results




    elif content_type == "application/json":
        section_results = []
        generated_pairings = request.json.get("pairings")
        file_name = request.json.get("file_name")
        # Validate format
        if validateJSONFormat(generated_pairings):
            sections = build_sections_from_JSON(generated_pairings)

            # Make solutions file
            index = request.json.get('index')
            #index = int(index)
            solution_file = resolve_testcase_index(index)

            if solution_file == "Invalid Test Case: Test case was not found. Make sure the section name is unchanged":
                return "Invalid Test Case: Test case was not found. Make sure the section name is unchanged"
            elif solution_file != resolve_testcase(sections[0].name):
                return "Invalid Test Case: Incorrect pairings file provided for the prompted testcase"
            with open(solution_file) as f:
                solution_object = json.loads(f.read())
            solutions = [Section(section) for section in solution_object['Sections']]

            # Get results for each section
            for i in range(len(sections)):
                section_results.append(sections[i].checkLastRound(solutions[i]))
        else:
            return 'Invalid JSON Object'
        return section_results


# Helper function
def resolve_testcase(testcase_name):
    '''
    This function will resolve which test cases we're testing by using the section name 
    and return the name to the appropriate soltuon file.
    '''
    initial_path = 'solutions/'
    parts = testcase_name.split('_')
    name = testcase_name.split('.')[0]
    if parts[0] in os.listdir(initial_path):
       if os.path.exists(initial_path + str(parts[0] + '/' + name + '_solution.json')):
           return str(initial_path + parts[0] + '/' + name + '_solution.json')
    return "Invalid Test Case: Test case was not found. Make sure the section name is unchanged"

def resolve_testcase_index(index):
    if index > 0 and index <= 75: # Number of test cases for t1
        test_cases = os.listdir("inputs/t1")
        test_cases.sort()
        return "solutions/t1/" + test_cases[index - 1].replace(".json", "_solution.json")
    elif index > 75 and index <= 159:
        test_cases = os.listdir("inputs/t2")
        test_cases.sort()
        return "solutions/t2/" + test_cases[index - 1 - 75].replace(".json", "_solution.json")
    elif index > 159 and index <= 247:
        test_cases = os.listdir("inputs/t3")
        test_cases.sort()
        return "solutions/t3/" +test_cases[index - 1 - 159].replace(".json", "_solution.json")
    elif index > 247 and index <= 335:
        test_cases = os.listdir("inputs/t4")
        test_cases.sort()
        return "solutions/t4/" + test_cases[index - 1 - 247].replace(".json", "_solution.json")
    elif index > 335 and index <= 402:
        test_cases = os.listdir("inputs/t5")
        test_cases.sort()
        return "solutions/t5/" + test_cases[index - 1 - 335].replace(".json", "_solution.json")
    else:
        return "Invalid test case index"


def resolve_index(index):
    # print(os.getcwd())
    if index > 0 and index <= 75: # Number of test cases for t1
        test_cases = os.listdir("inputs/t1")
        test_cases.sort()
        return test_cases[index - 1]
    elif index > 75 and index <= 159:
        test_cases = os.listdir("inputs/t2")
        test_cases.sort()
        return test_cases[index - 1 - 75]
    elif index > 159 and index <= 247:
        test_cases = os.listdir("inputs/t3")
        test_cases.sort()
        return test_cases[index - 1 - 159]
    elif index > 247 and index <= 335:
        test_cases = os.listdir("inputs/t4")
        test_cases.sort()
        return test_cases[index - 1 - 247]
    elif index > 335 and index <= 402:
        test_cases = os.listdir("inputs/t5")
        test_cases.sort()
        return test_cases[index - 1 - 335]
    else:
        return "Invalid test case index"

    
@app.route('/testcase', methods=['GET'])
def testcase():
    index = request.args.get('index')
    index = int(index)
  
    # Assuming you have a list of file names
    if index >= 0:
        
        tc = resolve_index(index)
        path_to_file = 'inputs/' + tc.split("_")[0] + '/' + tc

        # Check if the file exists
        if os.path.exists(path_to_file):
            return send_file(path_to_file)
        else:
            return 'Server error: File not found'
    else:
        return 'Invalid index'

@app.route('/solution', methods=['GET'])
def solution():
    index = request.args.get('index')
    index = int(index)
  
    # Assuming you have a list of file names
    if index >= 0:
        
        tc = resolve_index(index)
        path_to_file = 'solutions/' + tc.split("_")[0] + '/' + tc.split(".")[0] + "_solution.json"
        print(path_to_file)

        # Check if the file exists
        if os.path.exists(path_to_file):
            return send_file(path_to_file)
        else:
            return 'Server error: File not found'
    else:
        return 'Invalid index'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

