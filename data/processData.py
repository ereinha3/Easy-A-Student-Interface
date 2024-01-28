from gradeData import courseDict
from departmentData import departmentData
from crnData import crnData

from numpy import mean

def getCourseDepartment(courseName):
    return ''.join((x for x in courseName if not x.isdigit()))

def getCourseLevel(courseName):
    return int(''.join((x for x in courseName if x.isdigit())))

def getCoursesByDepartment(departmentName):
    courses = courseDict.keys()
    return [course for course in courses if getCourseDepartment(course) == departmentName]

def filterCoursesByLevel(courseList, level):
    return [course for course in courseList if getCourseLevel(course) // 100 == level // 100]

def getInstructorsByCourse(course):
    return [courseInstance["instructor"] for courseInstance in courseDict[course]]

def getCourseGrades(course):
    return { key : float(val) for key, val in course.items() if "prec" in key }

def getAllDepartments():
    return { getCourseDepartment(key) for key in courseDict }

def getCrnsByCourse(courseName):
    return { int(courseInstance["crn"]) for courseInstance in courseDict[courseName] }

def createDepartmentLevelDict():
    return { department : { getCourseLevel(course) : { crn for crn in getCrnsByCourse(course) } for course in courseDict } for department in getAllDepartments() }

def getGradeData(courseInstance):
    return {key.lower(): value for key, value in courseInstance.items() if key != "crn"}

def createCrnDict():
    crnDict = {}
    for courseName, courseListing in courseDict.items():
        for courseInstance in courseListing:
            crnDict[int(courseInstance["crn"])] = getGradeData(courseInstance) | {"course_name": courseName}
    return crnDict

def writeDataToFile(dataName, dataBody, filename):
    f = open(filename, 'w')
    f.write(dataName + " = " + str(dataBody))
    f.close()

writeDataToFile("departmentData", createDepartmentLevelDict(), "departmentData.py")
writeDataToFile("crnData", createCrnDict(), "crnData.py")

#print(augmentCrnData())

#print(breakCoursesByDepartmentAndLevel())
#print(getAllCourseInstances())

#breakCoursesByDepartmentAndLevel()

#Example for quick testing
#MathCourses = getCoursesByDepartment("MATH")
#Math200 = filterCoursesByLevel(MathCourses, 200)
#getInstructorsByCourse(Math200[0])
#print(getCourseGrades(courseDict[Math200[0]][0]))
