import os
import ast
from colorama import Fore, Style
from tqdm import tqdm
from settings import setting

class FileHandler:
    """
    历变更后的文件的循环中，为每个变更后文件（也就是当前文件）创建一个实例
    """
    def __init__(self, repo_path, file_path):
        self.file_path = file_path  # 这里的file_path是相对于仓库根目录的路径
        self.repo_path = repo_path
        self.project_hierarchy = setting.project.target_repo / setting.project.hierarchy_name
    

    def check_files_and_folders(self) -> list:
        """
        Check all files and folders in the given directory
        Return a list of files that are not ignored and have the '.py' extension.
        The returned file paths are relative to the self.directory.

        Returns:
            list: A list of paths to files that are not ignored and have the '.py' extension.
        """
        not_ignored_files = []
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [
                d
                for d in dirs
            ]

            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.repo_path)
                if file_path.endswith(".py"):
                    not_ignored_files.append(relative_path)

        return not_ignored_files
    
    def add_parent_references(self, node, parent=None):
        """
        Adds a parent reference to each node in the AST.

        Args:
            node: The current node in the AST.

        Returns:
            None
        """
        for child in ast.iter_child_nodes(node):
            child.parent = node
            self.add_parent_references(child, node)

    def get_end_lineno(self, node):
        """
        Get the end line number of a given node.

        Args:
            node: The node for which to find the end line number.

        Returns:
            int: The end line number of the node. Returns -1 if the node does not have a line number.
        """
        if not hasattr(node, "lineno"):
            return -1  # 返回-1表示此节点没有行号

        end_lineno = node.lineno
        for child in ast.iter_child_nodes(node):
            child_end = getattr(child, "end_lineno", None) or self.get_end_lineno(child)
            if child_end > -1:  # 只更新当子节点有有效行号时
                end_lineno = max(end_lineno, child_end)
        return end_lineno
    
    def get_obj_code_info(self, code_type, code_name, start_line, end_line, params, file_path = None):
        """
        Get the code information for a given object.

        Args:
            code_type (str): The type of the code.
            code_name (str): The name of the code.
            start_line (int): The starting line number of the code.
            end_line (int): The ending line number of the code.
            parent (str): The parent of the code.
            file_path (str, optional): The file path. Defaults to None.

        Returns:
            dict: A dictionary containing the code information.
        """

        code_info = {}
        code_info['type'] = code_type
        code_info['name'] = code_name
        code_info['md_content'] = []
        code_info['code_start_line'] = start_line
        code_info['code_end_line'] = end_line
        code_info['params'] = params

        with open(
            os.path.join(
                self.repo_path, file_path if file_path != None else self.file_path
            ),
            "r",
            encoding="utf-8",
        ) as code_file:
            lines = code_file.readlines()
            code_content = "".join(lines[start_line - 1 : end_line])
            # 获取对象名称在第一行代码中的位置
            name_column = lines[start_line - 1].find(code_name)
            # 判断代码中是否有return字样
            if "return" in code_content:
                have_return = True
            else:
                have_return = False

            code_info["have_return"] = have_return
            # # 使用 json.dumps 来转义字符串，并去掉首尾的引号
            # code_info['code_content'] = json.dumps(code_content)[1:-1]
            code_info["code_content"] = code_content
            code_info["name_column"] = name_column

        return code_info

    def get_functions_and_classes(self, code_content):
        """
        Retrieves all functions, classes, their parameters (if any), and their hierarchical relationships.
        Output Examples: [('FunctionDef', 'AI_give_params', 86, 95, None, ['param1', 'param2']), ('ClassDef', 'PipelineEngine', 97, 104, None, []), ('FunctionDef', 'get_all_pys', 99, 104, 'PipelineEngine', ['param1'])]
        On the example above, PipelineEngine is the Father structure for get_all_pys.

        Args:
            code_content: The code content of the whole file to be parsed.

        Returns:
            A list of tuples containing the type of the node (FunctionDef, ClassDef, AsyncFunctionDef),
            the name of the node, the starting line number, the ending line number, the name of the parent node, and a list of parameters (if any).
        """
        tree = ast.parse(code_content)
        self.add_parent_references(tree)
        functions_and_classes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                start_line = node.lineno
                end_line = self.get_end_lineno(node)
                parameters = [arg.arg for arg in node.args.args] if 'args' in dir(node) else []
                all_names = [item[1] for item in functions_and_classes]
                functions_and_classes.append(
                    (type(node).__name__, node.name, start_line, end_line, parameters)
                )
        return functions_and_classes

    def generate_file_structure(self, file_path):
        """
        Generates the file structure for the given file path.

        Args:
            file_path (str): The relative path of the file.

        Returns:
            dict: A dictionary containing the file path and the generated file structure.

        Output example:
        {
            "function_name": {
                "type": "function",
                "start_line": 10,
                ··· ···
                "end_line": 20,
                "parent": "class_name"
            },
            "class_name": {
                "type": "class",
                "start_line": 5,
                ··· ···
                "end_line": 25,
                "parent": None
            }
        }
        """
        with open(os.path.join(self.repo_path, file_path), "r", encoding="utf-8") as f:
            content = f.read()
            structures = self.get_functions_and_classes(content)
            file_objects = [] #以列表的形式存储
            for struct in structures:
                structure_type, name, start_line, end_line, params = struct
                code_info = self.get_obj_code_info(structure_type, name, start_line, end_line, params, file_path)
                file_objects.append(code_info)

        return file_objects

    def generate_overall_structure(self, file_path_reflections, jump_files) -> dict:

        repo_structure = {}
        bar = tqdm(self.check_files_and_folders())
        not_ignored_files = []
        for not_ignored_files in bar:
            normal_file_names = not_ignored_files
            try:
                repo_structure[normal_file_names] = self.generate_file_structure(
                    not_ignored_files
                )
            except Exception as e:
                print(
                    f"Alert: An error occurred while generating file structure for {not_ignored_files}: {e}"
                )
                continue
            bar.set_description(f"generating repo structure: {not_ignored_files}")
        return repo_structure