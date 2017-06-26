from django.db import models
from users.models import User
from treebeard.ns_tree import NS_Node
from treebeard.mp_tree import MP_Node
from django.core import serializers


class Post(models.Model):
    title = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    description = models.TextField(default='')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    node_order_by = ['created_at']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(MP_Node):
    name = models.CharField(blank=False, max_length=255)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    text = models.TextField(default='')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name + ' ' + str(self.id)

    @classmethod
    def dump_bulk(cls, parent=None, keep_ids=True, post_id=None):
        """Dumps a tree branch to a python data structure."""

        cls = get_result_class(cls)

        # Because of fix_tree, this method assumes that the depth
        # and numchild properties in the nodes can be incorrect,
        # so no helper methods are used
        qset = cls._get_serializable_model().objects.all()
        if parent:
            qset = qset.filter(path__startswith=parent.path)

        if post_id:
            qset = qset.filter(post_id=post_id)
        ret, lnk = [], {}
        for pyobj in serializers.serialize('python', qset):
            # django's serializer stores the attributes in 'fields'
            fields = pyobj['fields']
            path = fields['path']
            depth = int(len(path) / cls.steplen)
            # this will be useless in load_bulk
            del fields['depth']
            del fields['path']
            del fields['numchild']
            if 'id' in fields:
                # this happens immediately after a load_bulk
                del fields['id']

            newobj = {'data': fields}
            if keep_ids:
                newobj['id'] = pyobj['pk']

            if (not parent and depth == 1) or \
                    (parent and len(path) == len(parent.path)):
                ret.append(newobj)
            else:
                parentpath = cls._get_basepath(path, depth - 1)
                parentobj = lnk[parentpath]
                if 'children' not in parentobj:
                    parentobj['children'] = []
                parentobj['children'].append(newobj)
            lnk[path] = newobj
        return ret


def get_result_class(cls):
    base_class = cls._meta.get_field('path').model
    if cls._meta.proxy_for_model == base_class:
        return cls
    else:
        return base_class
