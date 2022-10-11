import pathlib

eng_path = pathlib.Path(pathlib.Path.cwd(), 'Eng')
list_of_course_name = [x.name for x in eng_path.iterdir() if x.is_dir()]
list_of_course_path = [x for x in eng_path.iterdir() if x.is_dir()]

list_course_level_path = [[x for x in list_of_course_path[i].iterdir() if x.is_dir()] for i in
                          range(len(list_of_course_path))]
list_course_level_name = [[x.name for x in list_of_course_path[i].iterdir() if x.is_dir()] for i in
                          range(len(list_of_course_path))]
list_course_level_descr = [[x for x in list_of_course_path[i].iterdir() if x.is_file()] for i in
                           range(len(list_of_course_path))]
