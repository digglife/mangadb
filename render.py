# -*- coding: utf8 -*-

from jinja2 import Environment, PackageLoader, select_autoescape

class Render():

    def __init__(self, template):
        package_loader = PackageLoader(__loader__.name)
        loader = FileSystemLoader(template) if template else package_loader
        self.env = Environment(loader=loader)

    def html(self, book):
        template = self.env.get_template('book.html')
        return template.render(book)

    def image(self, book):
        pass