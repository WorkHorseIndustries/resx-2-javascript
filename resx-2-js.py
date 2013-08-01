from xml.dom import minidom
import sys, os
import re

class ResourceToJs:
    """Scrapes .Net .resx (or any file implementing that xml schema)
     files and writes out the translations as attributes to javascript objects"""
    # a list of reserved words in javascript
    reserved_words = ['abstract', 'boolean', 'break', 'byte', 'case', 'catch',
                      'char', 'class', 'const', 'continue', 'debugger', 'default', 'delete',
                      'do', 'double', 'else', 'enum', 'export', 'extends', 'false', 'final',
                      'finally', 'float', 'for', 'function', 'goto', 'if', 'implements',
                      'imports', 'in', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
                      'null', 'package', 'private', 'protected', 'public', 'return', 'short',
                      'static', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
                      'transient', 'true', 'try', 'typeof', 'var', 'volatile', 'void', 'while',
                      'with']

    # if a string does not fit this format than it is not a valid javascript variable/property name
    js_format_re = re.compile(r"^[A-Za-z_\$]+[A-Za-z0-9_\$]*$")

    def is_valid_name(self, str):
        """ returns whether this string is a valid javascript object or
        property name

        arguments:
        str -- string representing a javascript variable name

        returns bool
        """

        return not (str in self.reserved_words or
                    self.js_format_re.match(str) is None)

    def format(self, str):
        """ encode, format or escape the values of the resource
         file according to your needs

         parameters:
         str -- a string to be encoded

         returns string
         """
        return str.replace('"', '\\"')

    def convert_resx(self, file_path):
        """ reads the data tags from a resx file and returns that information
        as a dictionary where the key is the data name attribute and the value
        is the text in the value tag

        parameters:
        file_path -- the path to the resourcce file or a file the implements the xml schema
        used in .net resource files.

        returns dictionary
        """
        dom = minidom.parse(file_path)
        resources = {}
        for data_el in dom.getElementsByTagName('data'):
            name = data_el.getAttribute('name')
            if self.is_valid_name(name):
                value_node = data_el.getElementsByTagName('value')[0].firstChild
                resources[name] = "" if value_node is None else self.format(value_node.nodeValue)
            else:
                print name + ' is an invalid javascript attribute'
        return resources


    def write(self, file_path, translations={},
              object_path='Translation', file_mode="w", encoding="utf8"):
        """ writes writes out to a file each translation as a javascript
        object attribute

        parameters:
        file_path -- a path to the file that will be written to
        translations -- a dicationary, the key will become the a javascript
        property name and the value will be the value for that property
        object_path -- represents the javascript object chain
        in the object chain
        file_mode -- the mode to open the file with

        """
        if object_path == '' or object_path is None:
            print "an object path is required"
            return
        js_file = open(file_path, file_mode)
        try:
            for name, val in translations.items():
                if self.is_valid_name(name):
                    translation = object_path + '.' + name + '="' + val + '";\n'
                    js_file.write(translation.encode(encoding))
                else:
                    print name + ' is an invalid javascript variable name'
        finally:
            js_file.close()


if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) < 2:
        print """requires arguments \n
        1) App_GlobalResources file path, \n
        2) path to javascript folder to write files to \n
        3) <optional> name of javascript object to use as translation object
         defaults to translations"""
        sys.exit(1)

    path_to_resource_folder = args[0]
    path_to_js_folder = args[1]

    print path_to_resource_folder + '\n'
    print path_to_js_folder + '\n'

    js_object_name = 'Translations' if len(args) < 3 else args[2]

    resource_writer = ResourceToJs()

    language_resources = {}
    language_re = re.compile(r".*\.([a-z\-]+)\.resx$")
    for root, dirs, files in os.walk(path_to_resource_folder):
        for resource_file in files:
            fullpath = os.path.join(root, resource_file)
            # this holds all the resource data in a dictionary
            if fullpath[-4:] != 'resx':
                continue
            translations = resource_writer.convert_resx(fullpath)
            # the language that this is translated into
            language_match = language_re.match(resource_file)
            if language_match is None:
                language = 'en-US'
            else:
                language = language_match.group(1)

            # we want to create and object path that mimics the file path relative to the
            # path_to_resource_folder. We also want to remove the language and file extension
            # from the file name when we are representing it as a js object.

            # 6 represents the "." preceding the language as well as the proceeding ".resx"
            # english is the default resource type so it doesn't have a language prefix,
            # this means we just need to omit ".resx" so the file_type_length is 4
            file_type_length = 5 if language == "en-US" else (len(language) + 6)
            js_object_path = fullpath[len(path_to_resource_folder)+1: -file_type_length]
            js_object_path = js_object_path.replace(' ', '').replace('-', '').replace('\\', '.')

            language_resources.setdefault(language, []).append((js_object_path, translations))


    def initiialize_objects(namespace, resources, file_path, encoding="utf8"):
        #collect js object paths
        object_chain = []
        if namespace:
            object_chain.append(namespace)

        for resource in resources:
            path = namespace
            for obj_path in (resource[0]).split('.'):
                path = obj_path if path == "" else path + "." + obj_path
                if path not in object_chain:
                    object_chain.append(path)


        #write the paths out to a file
        js_file = open(js_file_path, "w")
        try:
            for obj in object_chain:
                js_file.write(obj.encode(encoding) + '={};\n')
        finally:
            js_file.close()


    def write_resources(namespace, resources, file_path):
        for resource in resources:
            if namespace: 
                js_object_path = namespace + "." + resource[0]
            else:
                js_object_path = resource
            resource_writer.write(
                file_path,
                resource[1],
                js_object_path,
                "a"
            )

    for language, resources in language_resources.items():
        #recursively_initialize_js = True
        js_file_path = path_to_js_folder + '\\' + language + '.js'
        initiialize_objects(js_object_name, resources, js_file_path)
        write_resources(js_object_name, resources, js_file_path)
