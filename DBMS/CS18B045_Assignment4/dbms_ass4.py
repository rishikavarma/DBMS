import mysql.connector
from mysql.connector import Error
 
def createDatabaseConnection(hostName, userName, password, dbName):
   try:
       return mysql.connector.connect(
           host = hostName, user = userName, passwd = password, database = dbName
       )
   except Error as err:
       print(f"Error: '{err}'")
 
def checkIfExists(connection, tableNames, condition):
   res = readQuery(connection, f"SELECT COUNT(*) FROM {tableNames} WHERE {condition};")
   valCount = res[0][0]
   return valCount > 0
 
 
def executeQuery(connection, query):
   cursor = connection.cursor()
   try:
       cursor.execute(query)
       connection.commit()
   except Error as err:
       print(f"Error: '{err}'")
 
 
def readQuery(connection, query):
   cursor = connection.cursor()
   try:
       cursor.execute(query)
       result = cursor.fetchall()
       return result
   except Error as err:
       print(f"Error: '{err}'")
 
 
def addCourse(connection, departmentId, courseId, teacherId, classRoom):
   # Check for departmentId exists, teacherId exists, courseId does not exist
  if checkIfExists( connection, 'department', f'deptId = { departmentId } ') and checkIfExists( connection, 'professor', f'empId = { teacherId } '):
    
    executeQuery(connection, f"INSERT INTO course VALUES ( { rollNo }, { courseId }, \'even\', 2006, \'B\' );")
 
def addEnrollment(connection, rollNo, courseId):
   # Check for rollNo exists, teaching exists, prerequisites done in previous enrollment
  if checkIfExists( connection, 'student s, teaching t', f's.rollNo = { rollNo } and t.courseId = { courseId } and t.sem = \"even\" and t.year = 2006'):
   	preRequisites = readQuery(connection, f"SELECT preReqCourse FROM prerequisite WHERE courseId ={ courseId } ;")
    for prereq in preRequisites:
      if checkIfExists( connection, 'enrollment', f'courseId = { prereq } and rollNo = \"{ rollNo }\" and ( year < 2006 or ( year = 2006 and sem = \'odd\') ) and grade <> \'U\' ') == False:
        print( "Invalid enrollment: Prerequisites not complete.")
        return
    if checkIfExists( connection, 'enrollment', f' courseId = \'{ courseId }\' and rollNo = \"{ rollNo }\" and grade <> \'U\' and ( year < 2006 or ( year = 2006 and sem = \'odd\') )'):
      print( "Invalid enrollment: Student has passed this course before." )
      return
    if checkIfExists( connection, 'enrollment', f' courseId = \'{ courseId }\' and rollNo = \"{ rollNo }\" and year = 2006 and sem = \'even\''):
      print( "Invalid enrollment: Student has been enrolled." )
      return
    executeQuery(connection, f"INSERT INTO enrollment VALUES ( { rollNo }, { courseId }, \'even\', 2006, \'B\' );")
  else:
    print( "Invalid enrollment: Input incorrect." )
 
def main():
 
   pass
 
if __name__ == "__main__":
   main()
   connection = createDatabaseConnection('localhost', 'zeta', 'qawsedr', 'academic_insti')
   data = readQuery(connection, "SELECT * FROM professor;")
   for i in data:
       print(i)
