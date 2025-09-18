import pytest
class  Student:
    def __init__(self,first_name:str,last_name:str,major:str,year:int):

        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.year=year
        
@pytest.fixture
def  default_emp():
    return Student("John","Doe","Computer Science",3)
def test_person_initialization(default_emp):
    # student=Student("John","Doe","Computer Science",2)
    assert default_emp.first_name=="John","First name should be Jon"
    assert default_emp.last_name=="Doe","Last name should be Doe"
    assert default_emp.major=="Computer Science" 
    assert default_emp.year==3
    
        
        