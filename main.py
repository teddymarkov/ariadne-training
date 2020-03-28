from ariadne import (
    make_executable_schema,
    load_schema_from_path,
)
from ariadne.asgi import GraphQL

import db
from resolvers.comment import comment
from resolvers.mutation import mutation
from resolvers.post import post
from resolvers.query import query
from resolvers.user import user

type_defs = load_schema_from_path("./schema.graphql")


def get_context_value(request):
    return {
        'request': request,
        'db': db,
    }


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    user,
    post,
    comment,
)

app = GraphQL(
    schema,
    context_value=get_context_value,
    debug=True,
)
