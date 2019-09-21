from unittest import TestCase

# from cfgr.discover import get_classes

class TestDiscover(TestCase):
  def test_get_classes(self):
    # classes = get_classes()
    # self.assertEqual(classes, [])
    pass

    # def get_components_from(self, module, ignores=[]):
    #     comps = []
    #     # find component class inside the module
    #     for klass in module.__dict__.values():
    #         # skip ignored classes
    #         if klass in ignores:
    #             continue

    #         # only grab the classes that have config_name and create_components attributes
    #         if hasattr(klass, 'config_name') and hasattr(klass, 'create_components'):
    #             comps.append(klass)
    #     return comps

    # def _found_component_classes(self):
    #     import py2030.components as comp_modules
    #     from py2030.base_component import BaseComponent

    #     mods = self.options['modules'].copy() if 'modules' in self.options else [] # provided modules

    #     # got local (default py2030) modules
    #     for module_name in comp_modules.__all__:
    #         # ignore the __init__.py file
    #         # if module_name == '__init__':
    #         #     continue

    #         # import file
    #         mod = __import__('py2030.components.'+module_name, fromlist=['py2030.components'])
    #         mods.append(mod)

    #     klasses = []
    #     for module in mods:
    #         klasses += self.get_components_from(module, ignores=[BaseComponent])

    #     del comp_modules
    #     del BaseComponent
    #     # print('klasses: ',klasses)

    #     return klasses