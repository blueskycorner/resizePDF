import os
import resizePDF



def test_buildPDF():
    print(os.getcwd())
    filename = "test/doc.pdf"
    if (os.path.exists(filename)):
        os.remove(filename)
    
    imagesList = ["test/Data/2016-06_Alex_CP_Bulletin1ertrim-page1.jpg","test/Data/2016-06_Alex_CP_Bulletin1ertrim-page2.jpg","test/Data/2016-06_Alex_CP_Bulletin1ertrim-page3.jpg"]
    resizePDF.buildPDF(filename, imagesList)
    assert os.path.exists(filename) == True
    assert os.path.getsize(filename) == 2526493