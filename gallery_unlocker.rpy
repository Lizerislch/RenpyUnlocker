init -1000 python:
    _GalleryUnlockerMod = _GalleryUnlockerMod()

init 1000 python:
    _GalleryUnlockerMod.hook_hijacks()

init -2000 python:
    def _GalleryUnlockerMod():
        import renpy

        object = _object
        type   = _type
        dict   = _dict
        list   = _list
        set    = _set
        str    = unicode

        def Hook(obj, name):
            attr = getattr(obj, name)
            hooked.add((obj, name, attr))

            def Hook(func):
                def wrapper(*args, **kwargs):
                    return func(attr, *args, **kwargs)

                for v in (obj if obj.__class__ is type else obj.__class__).__mro__:
                    if name in v.__dict__:
                        if isinstance(v.__dict__[name], (staticmethod, classmethod)):
                            wrapper = staticmethod(wrapper)
                        break

                wrapper.__name__ = attr.__name__
                wrapper.__doc__  = attr.__doc__

                setattr(obj, name, wrapper)
            return Hook

        hooked = set()

        class GalleryUnlocker(object):
            __author__  = "ModAuthor"
            __name__    = "Universal Gallery Unlocker"
            __version__ = (23, 3, 20)

            @property
            def author(self):
                return self.__author__

            @property
            def name(self):
                return self.__name__

            @property
            def version(self):
                return "20" + "-".join(str(i).zfill(2) for i in self.__version__)

            def __str__(self):
                return "{} [{}] [{}]".format(self.name, self.version, self.author)

            @staticmethod
            def _swap(o):
                def s(o):
                    if o is False:
                        return True
                    if o is 0:
                        return 1
                    if o is "":
                        return " "
                    if isinstance(o, (set, list, tuple)):
                        return o.__class__(s(v) for v in o)
                    if isinstance(o, dict):
                        return o.__class__((k, s(v)) for (k, v) in o.items())
                    return o

                o = s(o)

                if isinstance(o, (set, list, dict)):
                    f = lambda *args: True
                    o = type(o.__class__.__name__, (o.__class__,), dict(__contains__=f))(o)

                return o

            def hook_hijacks(self):
                mod = self

                @Hook(renpy.exports, 'seen_label')
                def hijack(func, *args, **kwargs):
                    return True

                @Hook(renpy.exports, 'seen_image')
                def hijack(func, *args, **kwargs):
                    return True

                @Hook(renpy.exports, 'seen_audio')
                def hijack(func, *args, **kwargs):
                    return True

                @Hook(renpy.game.Persistent, '__getattr__')
                def hijack(func, self, name):
                    if name.startswith("_"):
                        return func(self, name)
                    else:
                        return True

                @Hook(renpy.game.Persistent, '__getattribute__')
                def hijack(func, self, name):
                    if name.startswith("_"):
                        return func(self, name)
                    else:
                        return mod._swap(func(self, name))

                @Hook(renpy.exports, 'utter_restart')
                def hijack(func, *args, **kwargs):
                    mod.unhook_hijacks()
                    return func(*args, **kwargs)

            def unhook_hijacks(self):
                while hooked:
                    setattr(*hooked.pop())

        return GalleryUnlocker()
