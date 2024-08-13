import json
import os
import shutil
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from colorama import Fore, Style
from tqdm import tqdm

from chat_engine import ChatEngine
from doc_meta_info import DocItem, DocItemStatus, MetaInfo, need_to_generate
from file_handler import FileHandler
from log import logger
from project_manager import ProjectManager
from settings import setting


class Runner:
    def __init__(self):
        self.absolute_project_hierarchy_path = setting.project.target_repo / setting.project.hierarchy_name

        self.project_manager = ProjectManager(
            repo_path=setting.project.target_repo, 
            project_hierarchy=setting.project.hierarchy_name
        )
        self.chat_engine = ChatEngine(project_manager=self.project_manager)

        if not self.absolute_project_hierarchy_path.exists():
            file_path_reflections = {}
            jump_files = []
            self.meta_info = MetaInfo.init_meta_info(file_path_reflections, jump_files)
            self.meta_info.checkpoint(
                target_dir_path=self.absolute_project_hierarchy_path
            )
        else:  #project_hierarchy
            self.meta_info = MetaInfo.from_checkpoint_path(
                self.absolute_project_hierarchy_path
            )

        self.meta_info.checkpoint(  # .project_doc_record
            target_dir_path=self.absolute_project_hierarchy_path
        )
        #self.runner_lock = threading.Lock() 


    def get_all_pys(self, directory):
        """
        Get all Python files in the given directory.

        Args:
            directory (str): The directory to search.

        Returns:
            list: A list of paths to all Python files.
        """
        python_files = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        return python_files
    
    def generate_doc_for_a_single_item(self, doc_item: DocItem):
        """为一个对象生成文档"""
        try:

            rel_file_path = doc_item.get_full_name()

            if not need_to_generate(doc_item, setting.project.ignore_list):
                print(f"Content ignored/Document generated, skipping: {doc_item.get_full_name()}")
            else:
                print(f" -- Generating document  {Fore.LIGHTYELLOW_EX}{doc_item.item_type.name}: {doc_item.get_full_name()}{Style.RESET_ALL}")
                file_handler = FileHandler(setting.project.target_repo, rel_file_path)
                response_message = self.chat_engine.generate_doc(
                    doc_item=doc_item,
                    file_handler=file_handler,
                )
                doc_item.md_content.append(response_message.content)
                doc_item.item_status = DocItemStatus.doc_up_to_date
                self.meta_info.checkpoint(
                    target_dir_path=self.absolute_project_hierarchy_path
                )
        except Exception as e:
            logger.info(f"Document generation failed after multiple attempts, skipping: {doc_item.get_full_name()}")
            logger.error("Error:", e)
            doc_item.item_status = DocItemStatus.doc_has_not_been_generated


    def first_generate(self):
        logger.info("Starting to generate documentation")
        check_task_available_func = partial(need_to_generate, ignore_list=setting.project.ignore_list)
        task_manager, task_dict = self.meta_info.get_topology(
            check_task_available_func
        )  # Get task_manager and task_dict
        # topology_list = [item for item in topology_list if need_to_generate(item, ignore_list)]
        before_task_len = len(task_manager)

        if not self.meta_info.in_generation_process:
            self.meta_info.in_generation_process = True
            logger.info("Init a new task-list")
        else:
            logger.info("Load from an existing task-list")
        # task_dict = {i: {"item_status": task.item_status, "full_name": task.get_full_name(), "dependencies": []} for i, task in enumerate(task_manager)} # Corrected structure
        self.meta_info.print_task_list(task_dict)
 
        # try:
        #     task_manager.sync_func = self.markdown_refresh
        #     threads = [
        #         threading.Thread(
        #             target=worker,
        #             args=(
        #                 task_manager,
        #                 process_id,
        #                 self.generate_doc_for_a_single_item,
        #             ),
        #         )
        #         for process_id in range(setting.project.max_thread_count)
        #     ]
        #     for thread in threads:
        #         thread.start()
        #     for thread in threads:
        #         thread.join()

        #     self.meta_info.document_version = (
        #         self.change_detector.repo.head.commit.hexsha
        #     )
        #     self.meta_info.in_generation_process = False
        #     self.meta_info.checkpoint(
        #         target_dir_path=self.absolute_project_hierarchy_path
        #     )
        #     logger.info(
        #         f"Successfully generated {before_task_len - len(task_manager.task_dict)} documents."
        #     )

        # except BaseException as e:
        #     logger.info(
        #         f"Finding an error as {e}, {before_task_len - len(task_manager.task_dict)} docs are generated at this time"
        #     )

    def markdown_refresh(self):
        """将目前最新的document信息写入到一个markdown格式的文件夹里(不管markdown内容是不是变化了)"""
        #with self.runner_lock:
            # 首先删除doc下所有内容，然后再重新写入
        markdown_folder = setting.project.target_repo / setting.project.markdown_docs_name
        if markdown_folder.exists():
            shutil.rmtree(markdown_folder)  
        os.mkdir(markdown_folder)  

        file_item_list = self.meta_info.get_all_files()
        for file_item in tqdm(file_item_list):

            def recursive_check(
                doc_item: DocItem,
            ) -> bool:  # 检查一个file内是否存在doc
                if doc_item.md_content != []:
                    return True
                for _, child in doc_item.children.items():
                    if recursive_check(child):
                        return True
                return False

            if recursive_check(file_item) == False:
                # logger.info(f"不存在文档内容，跳过：{file_item.get_full_name()}")
                continue
            rel_file_path = file_item.get_full_name()

            def to_markdown(item: DocItem, now_level: int) -> str:
                markdown_content = ""
                markdown_content += (
                    "#" * now_level + f" {item.item_type.to_str()} {item.obj_name}"
                )
                if (
                    "params" in item.content.keys()
                    and len(item.content["params"]) > 0
                ):
                    markdown_content += f"({', '.join(item.content['params'])})"
                markdown_content += "\n"
                markdown_content += f"{item.md_content[-1] if len(item.md_content) >0 else 'Doc is waiting to be generated...'}\n"
                for _, child in item.children.items():
                    markdown_content += to_markdown(child, now_level + 1)
                    markdown_content += "***\n"

                return markdown_content

            markdown = ""
            for _, child in file_item.children.items():
                markdown += to_markdown(child, 2)
            assert markdown != None, f"Markdown content is empty, the file path is: {rel_file_path}"
            # 写入markdown内容到.md文件
            file_path = os.path.join(
                setting.project.markdown_docs_name,
                file_item.get_file_name().replace(".py", ".md"),
            )
            if file_path.startswith("/"):
                # 移除开头的 '/'
                file_path = file_path[1:]
            abs_file_path = setting.project.target_repo / file_path
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            with open(abs_file_path, "w", encoding="utf-8") as file:
                file.write(markdown)

        logger.info(
            f"markdown document has been refreshed at {setting.project.markdown_docs_name}"
        )

    def run(self):
        """
        Runs the document update process.

        This method detects the changed Python files, processes each file, and updates the documents accordingly.

        Returns:
            None
        """
        self.first_generate()
        self.meta_info.checkpoint(
            target_dir_path=self.absolute_project_hierarchy_path,
            flash_reference_relation=True,
        ) 
        self.markdown_refresh()
       

       