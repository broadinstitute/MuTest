import os
import shutil

from SomaticFileSystem import *

class Dataset:
    def __init__(self,parent_dir,name):
        self.name = name
        self.location = os.path.join(parent_dir,name)

        if not os.path.exists(self.location):
            os.mkdir(self.location)

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def list_files(self):
        return os.listdir(self.location)

    def remove_file(self, filename):
        os.remove( os.path.join(self.location,filename) )

    def add_file(self,original):
        basename = os.path.basename(original)
        shutil.copy2(original, os.path.join(self.location, basename))

    def delete(self):
        shutil.rmtree(self.location)

    def __iter__(self):
        return iter(self.list_files())

class Project:
    def __init__(self,parent_dir,name):
        self.name = name
        self.location = os.path.join(parent_dir,name)

        if not os.path.exists(self.location):
            os.mkdir(self.location)

        datasets = os.listdir(self.location)
        datasets = [entry for entry in datasets if os.path.isdir( os.path.join(self.location,entry))]
        self.datasets = {entry:Dataset(self.location, entry) for entry in datasets}

    def list_datasets(self):
        return self.datasets

    def remove_dataset(self,name):
        if self.datasets.has_key(name):
            self.datasets[name].delete()
            del self.datasets[name]

    def add_dataset(self,name):
        self.datasets[name] = Dataset(self.location, name)

    def delete(self):
        shutil.rmtree(self.location)

    def __iter__(self):
        return iter(self.datasets.values())

    def __getitem__(self,name):
        return self.datasets[name]

class SomaticFileSystem:
    def __init__(self,location):
        self.location = location
        projects = os.listdir(self.location)
        projects = [project for project in projects if os.path.isdir( os.path.join(self.location,project))]
        self.projects = {project:Project(self.location, project) for project in projects}

    def list_projects(self):
        return self.projects

    def remove_project(self,name):
        if self.projects.has_key(name):
            self.projects[name].delete()
            del self.projects[name]

    def add_project(self,name):
        self.projects[name] = Project(self.location, name)

    def __getitem__(self,name):
        return self.projects[name]

    def __iter__(self):
        return iter(self.projects.values())

