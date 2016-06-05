
import unittest
import codecs
import StringIO
import xml2pro

class Test_XML2Pro(unittest.TestCase):
    def test_1(self):
        input_filename = 'test/An Affair to Remember.xml'
        model_filename = 'test/An Affair to Remember.pro.model'

        fout = StringIO.StringIO()
        x1 = xml2pro.XML2Pro(input_filename, fout)
        x1.process_file()
        
        generated_text = fout.getvalue()
        with codecs.open(model_filename, 'r', 'utf-8') as f:
            model_text = f.read()
            
        self.assertEqual(generated_text, model_text)


if __name__ == '__main__':
    unittest.run()
    
