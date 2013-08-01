resx-2-javascript
=================
Want to use Python to translate .net .resx file into javascript? Then I got you. 

Use
=================

Get access to your resource translations in javascript.

The resx-2-js.py takes 3 arguments
1) the path your App_Resources folder or whatever directory contains all your resource files/folders 
  (from this point on this will be refered to as the App_Resources folder)
2) the path to directory where you would like the javascript to be written
3)(optional) a javascript object that will contain each of the translations.  defaults to Translations


How it works
=================

The script recurses through the App_Resources file structure looking for resx files.  When it finds one it looks to 
the filename to identifiy the culture name e.g. Test.es.resx which identifies the culture name as es. If There
is no culture in the filename assumes en-US. After identifying the culture, gathers thats file's filepath relative to 
the App_Resources folder, (this will be used as the javascript object path) and collects each of the key value pairs 
in the resx file.

It script then writes to different javascript file for each language found.  Each file contain the translations for 
that culture.  The javascript object path mimics the folder structure, with each new object being initialized at the 
top of the file.

Example
=================
if your resource files looked something like this 

App_Resources

        -----> TestFolder
        
                Test.es.resx
                  Key      | Value
                  -----------------
                  one      | uno
                  two      | dos 
                
                Test.resx
                  Key      | Value
                  -----------------
                  one      | one
                  two      | two
          
        -----> NextFolder
        
                Test.ru.resx
                  Key      | Value
                  -----------------
                  hello    | привет
                
                Test.resx
                  Key      | Value
                  -----------------
                  hello    | hello
          
These files would be written to whatever directory was specified as the output directory

    en-US.js
      Translate = {};
      Translate.TestFolder = {};
      Translate.NextFolder = {};
      Translate.TestFolder.one = "one";
      Translate.TestFolder.two = "two";
      Translate.NextFolder.hello = "hello";

    es.js
      Translate = {};
      Translate.TestFolder = {};
      Translate.TestFolder.one = "uno";
      Translate.TestFolder.two = "dos";
      
    ru.js
      Translate = {};
      Translate.NextFolder = {};
      Translate.NextFolder.hello = "привет";
      
    If you specified the thrid argument than Translate would be whatever that was.


Notes
=================
outputs as utf8
directory names file names and keys in resx files must all be valid javascript attribute names

Disclaimer
=================
The code is not very efficient so I wouldn't use this at runtime.   I also haven't had time to 
clean it up yet so I'm sure that are many areas that could used quite a bit of improvment.  Please
Feel free to fork and do so. 




