from bs4 import BeautifulSoup as BS
import requests
# Downloaded html file because original website was .html and would not root to same page.
with open("C:\\Users\\Griffin Barros-King\\Documents\\Classes2023.html") as fp:
    soup = BS(fp, "html.parser")

# Website html was poorly documented so the  
# only unique thing that applied to all the lines 
# I was looking  for was that they were <td>.
course_nums = soup.findAll("td")

# Create dictionary to store 
# (key = class department, value = list of class ID's).
dict = {}
# iterate through lots of lines due to lack of consistant uniqueness.
for i in range(len(course_nums)):
    # Check if the line after the class department is the 
    # first class acronym line in department using the fact
    # that it contains a most recent day updated,
    # an identifier that makes it possibly a department.
    if course_nums[i].text.find("As of:") != -1:
        # Check if the line before it has another necessary identifier.
        if course_nums[i-2].text.find("TBA") == -1:
            newind = course_nums[i-1].text.find("   ")
            # Check one more identifier. Only way to guarentee it
            # is a in fact a department
            # if it is set it to the current key.
            if course_nums[i-1].text[3:newind].find("\t\t") == -1:
                currKey = course_nums[i-1].text[3:newind]
            # Check if the current department is already in the 
            # dictionary. If not make a new key in dictionary.
            if (currKey in dict) != True:
                dict[currKey] = []
        # First identifier for department conveniently
        # is the class acronym.
        
        # Class acronym is surrounded by parentheses in the line
        # first index is "(".
        index = course_nums[i].text.find("(")
        # Start right after the "(" and take the first 4 characters.
        # Class acronyms are at most 4 characters and if they are
        # less they will have spaces after due to formatting.

        # we save this as this is only half the class ID without the class
        # number.
        currClass = course_nums[i].text[index+1:index+5].strip()
    # Now we find the class numbers.
    # 
    # Check if line after contains "Units" as this is only 
    # consistent unique identifier for class numbers.
    if course_nums[i].text.find("Units") != -1:
        # There are multiple listings for the same course so
        # we find out if it has already been added to the dictionary.
        alreadyExists = False
        # Run through each value.
        for val in dict.values():
            # Check if the full ID matches any values.
            if ((currClass + " " + course_nums[i-1].text.strip()) in val) == True:
                alreadyExists = True
        # Check if it passed the all the checks.
        if alreadyExists == False:
            # Combine class acronym and number and add it to
            # the dictionary at the key of the current department.
            dict[currKey].append(currClass + " " + course_nums[i-1].text.strip())
   
# I needed to use this information to create a list of objects
# in js where each object contained the department of the class
# and class number.

# Opened file I already created(I just copied what was in the 
# text file to a java script file in the correct repository).
f = open("classes.txt", "a")
# Initiate the list.
f.write("const classes = [\n")
# Iterate through the departments.
for val in dict.keys():
    # Set current state of the department to nonexistent.
    departmentExists = False
    # Iterate through class IDs.
    for value in dict[val]:
        # If department doesnt exist add new object.
        if departmentExists == False:
            f.write("   {\n")
            f.write(f"       \'department\': \'{val}\',\n")
            stop = value.find(" ")
            f.write("       \'classes\': [\n")
            departmentExists = True
        # Add class ID to object.
        f.write(f"          \'{value}\',\n")
    f.write("       ]\n")
    f.write("   },\n")
f.write("]")
f.close()
#Done!!!
    