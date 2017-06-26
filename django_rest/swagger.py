from rest_framework.schemas import SchemaGenerator
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class MySchemaGenerator(SchemaGenerator):
    title = 'REST API Index'

    def get_link(self, path, method, view):
        link = super(MySchemaGenerator, self).get_link(path, method, view)
        link._fields += self.get_core_fields(view)
        return link

    def get_core_fields(self, view):
        return getattr(view, 'coreapi_fields', ())


class SwaggerSchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = MySchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
