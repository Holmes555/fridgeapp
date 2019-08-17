from rest_framework import schemas
from rest_framework_swagger.renderers import OpenAPICodec, OpenAPIRenderer


class OpenAPIRendererToFile(OpenAPIRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        options = self.get_customizations()

        return OpenAPICodec().encode(data, **options)


def run():
    generator = schemas.SchemaGenerator(title='Sunflower API')
    schema = generator.get_schema()
    renderer = OpenAPIRendererToFile()
    result = renderer.render(schema)
    with open('data.json', 'w+') as outfile:
        outfile.write(result.decode("utf-8"))
